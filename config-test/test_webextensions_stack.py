import configparser
import pytest
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


def test_add_content(env, conf):
    # Grab a bearer token that we can use to talk to the webextensions endpoint
    acct = TestEmailAccount()
    email = acct.email
    passwd = str(uuid.uuid4())
    fxaclient = FxaClient("https://api.accounts.firefox.com")
    session = fxaclient.create_account(email, passwd)
    m = acct.wait_for_email(lambda m: "x-verify-code" in m["headers"])

    if m is None:
        raise RuntimeErrors("Verification email did not arrive")

    session.verify_email_code(m["headers"]["x-verify-code"])
    auth = FxABearerTokenAuth(
        email,
        passwd,
        scopes=['sync:addon_storage'],
        client_id=DEFAULT_CLIENT_ID,
        account_server_url=conf.get(env, 'account_server_url'),
        oauth_server_url=conf.get(env, 'oauth_server_url'),
    )
    client = Client(server_url=conf.get(env, 'we_server_url'), auth=auth)

    # Add a record to our QA collection and make sure we have N+1 records
    existing_records = client.get_records(collection=conf.get(env, 'qa_collection'), bucket='default')
    assert len(existing_records) == 0

    data = {"payload": {"encrypted": "SmluZ28gdGVzdA=="}}
    resp = client.create_record(data, collection=conf.get(env, 'qa_collection'), bucket='default')
    new_record_id = resp['data']['id']
    updated_records = client.get_records(collection=conf.get(env, 'qa_collection'), bucket='default')
    assert len(updated_records) == len(existing_records) + 1

    client.delete_record(
        new_record_id,
        collection=conf.get(env, 'qa_collection'),
        bucket='default'
    )
    updated_records = client.get_records(collection=conf.get(env, 'qa_collection'), bucket='default')
    assert len(updated_records) == len(existing_records)

    # Clean up the account that we created for the test
    acct.clear()
    fxaclient.destroy_account(email, passwd)



