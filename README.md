[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/Kinto/kinto-integration-tests/blob/master/LICENSE)
[![travis](https://img.shields.io/travis/Kinto/kinto-integration-tests.svg?label=travis)](http://travis-ci.org/Kinto/kinto-integration-tests/)
[![updates](https://pyup.io/repos/github/Kinto/kinto-integration-tests/shield.svg)](https://pyup.io/repos/github/Kinto/kinto-integration-tests/)
[![Python 3](https://pyup.io/repos/github/Kinto/kinto-integration-tests/python-3-shield.svg)](https://pyup.io/repos/github/Kinto/kinto-integration-tests/)

# Summary
Tests for the Kinto server fall into 3 categories:

1. unit tests - located here: https://github.com/Kinto/kinto/tree/master/tests
2. loadtests - located here:  https://github.com/Kinto/kinto-loadtests
3. configuration check tests - located in this repo

This repo is a clearinghouse for all automated tests that don't need to reside in their own repository.
They would include a variety of test types that usually fall in the middle of the test pyramid:
API tests, config and URL checks, deployment tests, end-2-end tests, security tests, etc.

## Preparing the tests

To run the tests, you need to have the following installed:

* Python 3.6 or greater
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)


## Running the tests

You can run these tests using the following commands from inside the root directory for the project:

```shell
$ pipenv install
$ pipenv run pytest -m TEST_TYPE --env TEST_ENV
```

* `TEST_TYPE` is `dist` for `kinto-dist` deployments, `settings` for `kinto-settings` deployments and `webextensions` for `kintowe` deployments
* `TEST_ENV` is one of the environments listed in the `manifest.ini` file.

### Running the tests using Docker

With [Docker](https://www.docker.com) installed, running the tests is as simple as first building:

```shell
$ docker build -t kinto-tests .
```

Then, you can run the tests like so (substituting your TEST_TYPE and TEST_ENV):
```shell
$ docker run -it kinto-tests pytest -m settings --env=stage
```
