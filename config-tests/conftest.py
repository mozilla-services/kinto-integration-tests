# Configuration file for running contract-tests
import configparser
import pytest
import ssl

# Hack because of how SSL certificates are verified by default in Python
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        dest="env",
        default="stage",
        help="Environment tests are running in: stage or prod"
    )

    parser.addoption(
        "--api-version",
        dest="apiversion",
        help="Optional param: version of API under test"
    )


@pytest.fixture(scope="module")
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


@pytest.fixture(scope="module")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="module")
def apiversion(request):
    return request.config.getoption("--api-version")
