import asyncio
import configparser
import pytest
from smwogger import API

from fxtesteng.helpers import aslist


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
async def test_server_info(api, conf, env):
    res = await api.server_info()
    data = await res.json()
    expected_fields = aslist(conf.get(env, 'server_info_fields'))

    for key in data:
        assert key in expected_fields

    for field in expected_fields:
        assert field in data


@pytest.mark.asyncio
async def test_contribute(api, conf, env):
    res = await api.contribute()
    data = await res.json()
    expected_fields = aslist(conf.get(env, 'contribute_fields'))

    for key in data:
        assert key in expected_fields

    for field in expected_fields:
        assert field in data


@pytest.mark.asyncio
async def test_get_changess(api, conf, env):
    res = await api.get_changess()
    data = await res.json()

    for record in data['data']:
        assert 'host' in record

