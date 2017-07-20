import configparser
import pytest
import requests

from kinto_http import Client, KintoException


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


def test_fennec_dlc_exists(env, conf):
    client = Client(
        server_url=conf.get(env, 'reader_server'),
        bucket='fennec',
        collection='catalog'
    )
    records = client.get_records(_sort='-last_modified')

    '''
    {'attachment': {
        'filename': 'ClearSans-Regular.ttf.gz',
        'size': 70411,
        'mimetype': 'application/x-gzip',
        'original': 
            {'filename': 'ClearSans-Regular.ttf',
            'size': 142572,
            'mimetype': 'application/x-font-ttf',
            'hash': '9b91bbdb95ffa6663da24fdaa8ee06060cd0a4d2dceaf1ffbdda00e04915ee5b'
            }, 
        'location': 'fennec/catalog/78205bf8-c668-41b1-b68f-afd54f98713b.gz',
        'hash': 'a72f1420b4da1ba9e6797adac34f08e72f94128a85e56542d5e6a8080af5f08a'
        },
        'id': 'b887012a-01e1-7c94-fdcb-ca44d5b974a2', 'type': 'asset-archive', 'last_modified': 1467303410985, 'kind': 'font'}
    '''

    for record in records:
        content = conf.get(env, 'reader_server') + '/buckets/' + record['attachment']['location']
        resp = requests.get(content)
        status_code = resp.status_code
        assert status_code != 404
