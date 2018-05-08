import configparser
import pytest
import ssl

from dotenv import load_dotenv, find_dotenv


# Hack because of how SSL certificates are verified by default in Python
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# Load our dotenv file
load_dotenv(find_dotenv())


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

    parser.addoption(
        "--qa-collection-user",
        dest="qauser",
        help="Optional param: user who can access QA collection in staging"
    )

    parser.addoption(
        "--qa-collection-passwd",
        dest="qa_passwd",
        help="Optional param: password for user who can access QA collection in staging"
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


@pytest.fixture(scope="session")
def qauser(pytestconfig):
    return pytestconfig.getoption('--qa-collection-user')


@pytest.fixture(scope="session")
def qapasswd(pytestconfig):
    return pytestconfig.getoption("--qa-collection-passwd")
