import asyncio
import configparser
import pytest
from pyramid.compat import string_types
from smwogger import API


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
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="module")
def api(event_loop, conf, env):
    return API(conf.get(env, 'api_definition'), loop=event_loop)


@pytest.mark.asyncio
@pytest.mark.dist
async def test_version(api, conf, env, apiversion):
    res = await api.__version__()
    data = await res.json()
    expected_fields = aslist(conf.get(env, 'version_fields'))

    # First, make sure that data only contains fields we expect
    for key in data:
        assert key in expected_fields

    # Then make the we only have the expected fields in the data
    for field in expected_fields:
        assert field in data

    # If we're passed an API version via the CLI, verify it matches
    if apiversion:
        assert apiversion == data['version']


@pytest.mark.asyncio
@pytest.mark.dist
async def test_heartbeat(api, conf, env):
    res = await api.__heartbeat__()
    data = await res.json()
    expected_fields = aslist(conf.get(env, 'heartbeat_fields'))

    # First, make sure that data only contains fields we expect
    for key in data:
        assert key in expected_fields

    # Then make the we only have the expected fields in the data
    for field in expected_fields:
        assert field in data


@pytest.mark.asyncio
@pytest.mark.dist
async def test_server_info(api, conf, env):
    res = await api.server_info()
    data = await res.json()
    expected_fields = aslist(conf.get(env, 'server_info_fields'))

    for key in data:
        assert key in expected_fields

    for field in expected_fields:
        assert field in data


@pytest.mark.asyncio
@pytest.mark.dist
async def test_contribute(api, conf, env):
    res = await api.contribute()
    data = await res.json()
    expected_fields = aslist(conf.get(env, 'contribute_fields'))

    for key in data:
        assert key in expected_fields

    for field in expected_fields:
        assert field in data


@pytest.mark.asyncio
@pytest.mark.dist
async def test_get_changes(api, conf, env):
    res = await api.get_changess()
    data = await res.json()

    for record in data['data']:
        assert 'host' in record
