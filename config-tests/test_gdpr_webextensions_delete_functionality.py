import configparser
import pytest
import time
from fxa.__main__ import DEFAULT_CLIENT_ID
from fxa.plugins.requests import FxABearerTokenAuth
from kinto_http import Client, KintoException


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


@pytest.mark.webextensions
def test_delete_request_removes_data(conf, env, fxa_account, fxa_urls, fxa_client):
    if env == 'prod':
        pytest.skip('kintowe GDPR tests are not run in production')

    auth = FxABearerTokenAuth(
        fxa_account.email,
        fxa_account.password,
        scopes=['sync:addon_storage'],
        client_id=DEFAULT_CLIENT_ID,
        account_server_url=fxa_urls['authentication'],
        oauth_server_url=fxa_urls['oauth'],
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

    # Get the aliases of the bucket we are putting data in and
    # make sure that an unauthenticated user can see these records
    # before we delete the account
    we_bucket_id = we_client.server_info()["user"]["bucket"]
    anon_we_client = Client(server_url=conf.get(env, 'we_server_url'))
    resp = anon_we_client.get_record(
        id=we_record_id,
        bucket=we_bucket_id,
        collection=conf.get(env, 'qa_collection'))
    assert resp['data']['id'] == we_record_id

    # Delete FxA account
    fxa_client.destroy_account(fxa_account.email, fxa_account.password)

    # Wait 1 minute and then make sure the records do not exist because the
    # Kinto client will throw an exception for non-existent records
    time.sleep(60)
    with pytest.raises(KintoException):
        resp = anon_we_client.get_record(
            id=we_record_id,
            bucket=we_bucket_id,
            collection=conf.get(env, 'qa_collection'))
