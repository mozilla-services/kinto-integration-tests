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


@pytest.mark.notes
def test_delete_request_removes_data(conf, env, fxa_account, fxa_urls, fxa_client):
    if env == 'prod':
        pytest.skip('testpilot GDPR tests are not run in production')

    auth = FxABearerTokenAuth(
        fxa_account.email,
        fxa_account.password,
        client_id=DEFAULT_CLIENT_ID,
        scopes=["https://identity.mozilla.com/apps/notes"],
        account_server_url=fxa_urls['authentication'],
        oauth_server_url=fxa_urls['oauth'],
    )

    # Add some data to the Notes collection
    tp_client = Client(server_url=conf.get(env, 'tp_server_url'), auth=auth)
    tp_existing_records = tp_client.get_records(collection='notes', bucket='default')
    assert len(tp_existing_records) == 0
    data = {"subject": "QA Test", "value": "This stuff should get deleted"}
    tp_record = tp_client.create_record(
        data=data,
        collection='notes',
        permissions={"read": ["system.Everyone"]}
    )
    tp_record_id = tp_record['data']['id']
    tp_updated_records = tp_client.get_records(collection='notes', bucket='default')
    assert len(tp_updated_records) == len(tp_existing_records) + 1

    # Get the aliases of the bucket we are putting data in and
    # make sure that an unauthenticated user can see these records
    # before we delete the account
    print(tp_client.server_info()["user"])
    tp_bucket_id = tp_client.server_info()["user"]["bucket"]
    anon_tp_client = Client(server_url=conf.get(env, 'tp_server_url'))
    resp = anon_tp_client.get_record(
        id=tp_record_id,
        bucket=tp_bucket_id,
        collection='notes')
    assert resp['data']['id'] == tp_record_id

    # Delete FxA account
    fxa_client.destroy_account(fxa_account.email, fxa_account.password)

    # Wait 5 minutes and then make sure the records do not exist because the
    # Kinto client will throw an exception for non-existent records
    time.sleep(120)

    with pytest.raises(KintoException):
        resp = anon_tp_client.get_record(
            id=tp_record_id,
            bucket=tp_bucket_id,
            collection='notes')
