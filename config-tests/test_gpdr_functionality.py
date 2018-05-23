import configparser
import requests
import pytest
import time
import uuid
from fxa.__main__ import DEFAULT_CLIENT_ID
from fxa.core import Client as FxaClient
from fxa.plugins.requests import FxABearerTokenAuth
from fxa.tests.utils import TestEmailAccount
from kinto_http import Client


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


def test_delete_request_removes_data(conf, env):
    # Create a test user on FxA
    acct = TestEmailAccount()
    email = acct.email
    passwd = str(uuid.uuid4())
    fxaclient = FxaClient("https://api.accounts.firefox.com")
    session = fxaclient.create_account(email, passwd)
    m = acct.wait_for_email(lambda m: "x-verify-code" in m["headers"])

    if m is None:
        raise RuntimeError("Verification email did not arrive")

    session.verify_email_code(m["headers"]["x-verify-code"])
    auth = FxABearerTokenAuth(
        email,
        passwd,
        scopes=['sync:addon_storage', 'https://identity.mozilla.com/apps/notes'],
        client_id=DEFAULT_CLIENT_ID,
        account_server_url=conf.get(env, 'account_server_url'),
        oauth_server_url=conf.get(env, 'oauth_server_url'),
    )

    # Add some data to chrome.storage (kintowe)
    we_client = Client(server_url=conf.get(env, 'we_server_url'), auth=auth)
    we_existing_records = we_client.get_records(collection=conf.get(env, 'qa_collection'), bucket='default')
    assert len(we_existing_records) == 0
    data = {"payload": {"encrypted": "SmluZ28gdGVzdA=="}}
    we_record = we_client.create_record(
        data=data,
        collection=conf.get(env, 'qa_collection'),
        bucket='default',
        permissions={"read": ["system.Everyone"]}
    )
    we_record_id = we_record['data']['id']
    we_updated_records = we_client.get_records(collection=conf.get(env, 'qa_collection'), bucket='default')
    assert len(we_updated_records) == len(we_existing_records) + 1

    # Add data to Notes (kintotp)
    tp_client = Client(server_url=conf.get(env, 'tp_server_url'), auth=auth)
    tp_existing_records = tp_client.get_records(collection='notes', bucket='default')
    assert len(tp_existing_records) == 0
    data = {"subject": "QA Test", "value": "This stuff should get deleted"}
    tp_record = tp_client.create_record(
        data=data,
        collection='notes',
        bucket='default',
        permissions={"read": ["system.Everyone"]}
    )
    tp_record_id = tp_record['data']['id']
    tp_updated_records = tp_client.get_records(collection='notes', bucket='default')
    assert len(tp_updated_records) == len(tp_existing_records) + 1

    # Get the aliases of the buckets we are putting data in and
    # make sure that an unauthenticated user can see these records
    # before we delete the account
    we_bucket_id = we_client.server_info()["user"]["bucket"]
    resp = requests.get(
        conf.get(env, 'we_server_url') +
        '/buckets/{0}/collections/qa_collection/records/{1}'.format(we_bucket_id, we_record_id))
    assert resp.status_code == 200
    tp_bucket_id = tp_client.server_info()["user"]["bucket"]
    resp = requests.get(
        conf.get(env, 'tp_server_url') +
        '/buckets/{0}/collections/notes/records/{1}'.format(tp_bucket_id, tp_record_id))
    assert resp.status_code == 200

    # Delete FxA account
    acct.clear()
    fxaclient.destroy_account(email, passwd)

    # Wait 5 minutes and then make sure the records do not exist
    time.sleep(301)
    resp = requests.get(
        conf.get(env, 'we_server_url') +
        '/buckets/{0}/collections/qa_collection/records/{1}'.format(we_bucket_id, we_record_id))
    assert resp.status_code > 400
    tp_bucket_id = tp_client.server_info()["user"]["bucket"]
    resp = requests.get(
        conf.get(env, 'tp_server_url') +
        '/buckets/{0}/collections/notes/records/{1}'.format(tp_bucket_id, tp_record_id))
    assert resp.status_code > 400
