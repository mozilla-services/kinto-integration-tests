import pytest
import requests


def aslist_cronly(value):
    """ Split the input on lines if it's a valid string type"""
    if isinstance(value, str):
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
    fields = set(data.keys())
    expected_fields = {"source", "commit", "version", "build"}

    assert len(fields ^ expected_fields) == 0


@pytest.mark.dist
@pytest.mark.settings
@pytest.mark.webextensions
def test_heartbeat(conf, env, api_url):
    res = requests.get(api_url + '__heartbeat__')
    data = res.json()
    fields = set(data.keys())
    expected_fields = set(aslist(conf.get(env, 'heartbeat_fields')))

    assert len(fields ^ expected_fields) == 0


@pytest.mark.dist
@pytest.mark.settings
@pytest.mark.webextensions
def test_server_info(conf, env, api_url):
    res = requests.get(api_url)
    data = res.json()
    fields = set(data.keys())
    expected_fields = {
        "url", "project_docs", "project_name", "capabilities",
        "project_version", "settings", "http_api_version"
    }

    assert len(fields ^ expected_fields) == 0


@pytest.mark.dist
@pytest.mark.settings
@pytest.mark.webextensions
def test_contribute(conf, env, api_url):
    res = requests.get(api_url + 'contribute.json')
    data = res.json()
    fields = set(data.keys())
    expected_fields = {
        "keywords", "participate", "repository",
        "description", "urls", "name",
    }

    assert len(fields ^ expected_fields) == 0
