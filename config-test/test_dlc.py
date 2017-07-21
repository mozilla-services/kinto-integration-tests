import configparser
import hashlib
import pytest
import requests


from kinto_http import Client, KintoException


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


def test_fennec_dlc_exists(env, conf):
    r = requests.get(conf.get(env, 'font_collection'))
    response = r.json()

    for record in response['data']:
        # Make sure it's a type of record we're expecting
        assert 'kind' in record or 'hyphenation' in record

        # Make sure the file exists
        response = requests.get(conf.get(env, 's3_location') + record['attachment']['location'])
        assert response.status_code != 404
        assert len(response.content) > 0

        # Check the file hash matches
        m = hashlib.sha256()
        m.update(response.content)
        assert record['attachment']['hash'] == m.hexdigest()


