import configparser
import pytest
from fxa.__main__ import DEFAULT_CLIENT_ID
from fxa.plugins.requests import FxABearerTokenAuth
from kinto_http import Client
from pytest_testrail.plugin import pytestrail


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


@pytest.mark.webextensions
@pytestrail.case('C122566')
def test_add_content(env, conf, fxa_account, fxa_urls):
    if env == 'prod':
        pytest.skip('qa cannot create records in production')

    auth = FxABearerTokenAuth(
        fxa_account.email,
        fxa_account.password,
        scopes=['sync:addon_storage'],
        client_id=DEFAULT_CLIENT_ID,
        account_server_url=fxa_urls['authentication'],
        oauth_server_url=fxa_urls['oauth'],
    )
    client = Client(server_url=conf.get(env, 'we_server_url'), auth=auth)

    # Add a record to our QA collection and make sure we have N+1 records
    existing_records = client.get_records(collection=conf.get(env, 'qa_collection'), bucket='default')
    assert len(existing_records) == 0

    data = {"payload": {"encrypted": "SmluZ28gdGVzdA=="}}
    resp = client.create_record(data=data, collection=conf.get(env, 'qa_collection'), bucket='default')
    new_record_id = resp['data']['id']
    updated_records = client.get_records(collection=conf.get(env, 'qa_collection'), bucket='default')
    assert len(updated_records) == len(existing_records) + 1

    client.delete_record(id=new_record_id, collection=conf.get(env, 'qa_collection'))
    updated_records = client.get_records(collection=conf.get(env, 'qa_collection'), bucket='default')
    assert len(updated_records) == len(existing_records)
