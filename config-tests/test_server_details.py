import pytest
from pyramid.compat import string_types
import requests


def aslist_cronly(value):
    """ Split the input on lines if it's a valid string type"""
    if isinstance(value, string_types):
        value = filter(None, [x.strip() for x in value.splitlines()])
    return list(value)


def aslist(value, flatten=True):
    """ Return a list of strings, separating the input based on newlines
        and, if flatten=True (the default), also split on spaces within
        each line."""
    values = aslist_cronly(value)
    if not flatten:
        return values
    result = []
    for value in values:
        subvalues = value.split()
        result.extend(subvalues)
    return result


@pytest.fixture(scope="module")
def api_url(conf, env, request):
    api_url = 'dist_api'

    if 'settings' in request.node.keywords:
        api_url = 'settings_api'
    elif 'webextensions' in request.node.keywords:
        api_url = 'webextensions_api'

    return conf.get(env, api_url)


@pytest.mark.dist
@pytest.mark.settings
@pytest.mark.webextensions
def test_version(conf, env, api_url):
    data = requests.get(api_url + '__version__').json()
    expected_fields = aslist(conf.get(env, 'version_fields'))

    for key in data:
        assert key in expected_fields

    # Then make the we only have the expected fields in the data
    for field in expected_fields:
        assert field in data


@pytest.mark.dist
@pytest.mark.settings
@pytest.mark.webextensions
def test_heartbeat(conf, env, api_url):
    res = requests.get(api_url + '__heartbeat__')
    data = res.json()
    expected_fields = aslist(conf.get(env, 'heartbeat_fields'))

    # First, make sure that data only contains fields we expect
    for key in data:
        assert key in expected_fields

    # Then make the we only have the expected fields in the data
    for field in expected_fields:
        assert field in data


@pytest.mark.dist
@pytest.mark.settings
@pytest.mark.webextensions
def test_server_info(conf, env, api_url):
    res = requests.get(api_url)
    data = res.json()
    expected_fields = aslist(conf.get(env, 'server_info_fields'))

    for key in data:
        assert key in expected_fields

    for field in expected_fields:
        assert field in data


@pytest.mark.dist
@pytest.mark.settings
@pytest.mark.webextensions
def test_contribute(conf, env, api_url):
    res = requests.get(api_url + 'contribute.json')
    data = res.json()
    expected_fields = aslist(conf.get(env, 'contribute_fields'))

    for key in data:
        assert key in expected_fields

    for field in expected_fields:
        assert field in data
