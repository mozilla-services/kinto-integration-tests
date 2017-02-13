import configparser
import pytest
from fxa.__main__ import DEFAULT_CLIENT_ID
from fxa.plugins.requests import FxABearerTokenAuth
from kinto_http import Client


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


def test_add_content(env, conf):
    # Grab a bearer token that we can use to talk to the webextensions endpoint
    email = conf.get(env, 'fxa_user_email')
    passwd = conf.get(env, 'fxa_user_password')
    auth = FxABearerTokenAuth(
        email,
        passwd,
        scopes=['sync:addon_storage'],
        client_id=DEFAULT_CLIENT_ID,
        account_server_url=conf.get(env, 'account_server_url'),
        oauth_server_url=conf.get(env, 'oauth_server_url'),
    )
    client = Client(
        server_url=conf.get(env, 'we_server_url'),
        auth=auth
    )

    # First, we need to have one more more collections
    collections = client.get_collections('default')
    assert len(collections) > 0

    # Add a record to our QA collection and make sure we have N+1 records
    existing_records = client.get_records(conf.get(env, 'qa_collection'), 'default')
    assert len(existing_records) > 0
    data = {"payload": {"encrypted": "SmluZ28gdGVzdA=="}}
    resp = client.create_record(
        data,
        collection=conf.get(env, 'qa_collection'),
        bucket='default',
    )
    new_record_id = resp['data']['id']
    updated_records = client.get_records(conf.get(env, 'qa_collection'), 'default')
    assert len(updated_records) == len(existing_records) + 1

    client.delete_record(
        new_record_id,
        collection=conf.get(env, 'qa_collection'),
        bucket='default'
    )
    updated_records = client.get_records(conf.get(env, 'qa_collection'), 'default')
    assert len(updated_records) == len(existing_records)


