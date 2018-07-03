import datetime
from xml.dom import minidom

import configparser
import pytest
import requests
from kinto_signer.serializer import canonical_json
from kinto_signer.signer.local_ecdsa import ECDSASigner
from kinto_http import Client, KintoException
from pytest_testrail.plugin import pytestrail


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


def get_collection_data(client):
    collection = client.get_collection()
    records = client.get_records(_sort='-last_modified')
    timestamp = client.get_records_timestamp()
    return collection, records, timestamp


def verify_signer_id(collection, key_name):
    return collection['data']['signature']['signer_id'] == key_name


def verify_signatures(collection, records, timestamp):
    try:
        serialized = canonical_json(list(records), timestamp)
        signature = collection['data']['signature']
        with open('pub', 'w') as f:
            f.write(signature['public_key'])
        signer = ECDSASigner(public_key='pub')
        return signer.verify(serialized, signature) is None
    except KintoException as e:
        if e.response.status_code == 401:
            return -1
        return 0


@pytestrail.case('C122561')
@pytest.mark.settings
def test_addons_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'reader_server'),
        bucket='blocklists',
        collection='addons'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        if len(records) == 0:
            pytest.skip('blocklists/addons has no records')
        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'onecrl_key') or verify_signer_id(collection, 'remotesettings_key')
    except KintoException as e:
        if e.response.status_code == 401:
            pytest.fail('blocklists/addons does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))


@pytestrail.case('C122562')
@pytest.mark.settings
def test_plugins_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'reader_server'),
        bucket='blocklists',
        collection='plugins'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        if len(records) == 0:
            pytest.skip('blocklists/plugins has no records')
        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'remotesettings_key')
    except KintoException as e:
        if e.response.status_code == 401:
            pytest.fail('blocklists/plugins does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))


@pytestrail.case('C122563')
@pytest.mark.settings
def test_gfx_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'reader_server'),
        bucket='blocklists',
        collection='gfx'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        if len(records) == 0:
            pytest.skip('blocklists/gfx contains no records')
        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'remotesettings_key') or verify_signer_id(collection, 'onecrl_key')
    except KintoException as e:
        if e.response.status_code == 401:
            pytest.fail('blocklists/gfx does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))


@pytestrail.case('C122564')
@pytest.mark.settings
def test_certificates_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'reader_server'),
        bucket='blocklists',
        collection='certificates'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        if len(records) == 0:
            pytest.skip('No records in blocklists/certifications')

        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'onecrl_key')
    except KintoException as e:
        if e.response.status_code == 401:
            pytest.fail('blocklists/certificates does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))


@pytestrail.case('C122565')
@pytest.mark.settings
def test_certificate_pinning_signatures(env, conf):
    client = Client(
        server_url=conf.get(env, 'reader_server'),
        bucket='pinning',
        collection='pins'
    )
    try:
        collection, records, timestamp = get_collection_data(client)
        if len(records) == 0:
            pytest.skip('No records in pinning/pins')

        assert verify_signatures(collection, records, timestamp)
        assert verify_signer_id(collection, 'pinningpreload_key')
    except KintoException as e:
        if e.response.status_code == 401:
            pytest.fail('pinning/pins does not exist')
        pytest.fail('Something went wrong: %s %s' % (e.response.status_code, e.response))


@pytestrail.case('C122566')
@pytest.mark.settings
def test_blocklist_timestamp(env, conf):
    if env == 'prod':
        pytest.skip('Skipping blocklist timestamp test in production')

    client = Client(
        server_url=conf.get(env, 'reader_server'),
        bucket='blocklists'
    )
    # Take the highest timestamp of the collections contained in the blocklist.xml.
    last_modified = -1
    for cid in ('addons', 'plugins', 'gfx'):
        records = client.get_records(collection=cid, _sort='-last_modified',
                                     _limit=1, enabled='true')
        if len(records) > 0:
            last_modified = max(last_modified, records[0]['last_modified'])

    # Read the current XML blocklist ETag.
    blocklist_uri = conf.get(env, 'reader_server').strip('/') + (
        '/blocklist/3/{ec8030f7-c20a-464f-9b0e-13a3a9e97384}/58.0'
        '/Firefox/20180123185941/Darwin_x86_64-gcc3-u-i386-x86_64'
        '/en-US/release/Darwin 17.4.0/default/default/invalid/invalid/0/')
    r = requests.get(blocklist_uri)
    r.raise_for_status()
    etag_header = int(r.headers.get('ETag', '')[1:-1])
    last_modified_header = r.headers.get('Last-Modified', '')
    last_modified_header = datetime.datetime.strptime(last_modified_header,
                                                      '%a, %d %b %Y %H:%M:%S GMT')

    # Check XML attribute <blocklist lastupdate="1483471392954">
    dom = minidom.parseString(r.text)
    root = dom.getElementsByTagName('blocklist')[0]
    last_modified_attr = int(root.getAttribute('lastupdate'))

    # Make sure they all match.
    # See https://bugzilla.mozilla.org/show_bug.cgi?id=1436469
    assert last_modified == etag_header
    last_modified_dt = datetime.datetime.utcfromtimestamp(last_modified / 1000.0)
    assert last_modified_dt.replace(microsecond=0) == last_modified_header
    assert last_modified == last_modified_attr
