# Summary
Tests for the Kinto server fall into 3 categories:

1. unit tests - located here: https://github.com/Kinto/kinto/tests
2. loadtests - located here:  https://github.com/Kinto/kinto-loadtests
3. configuration check tests - located in this repo

This repo is a clearinghouse for all automated tests that don't need to reside in their own repository.
They would include a variety of test types that usually fall in the middle of the test pyramid:
API tests, config and URL checks, deployment tests, end-2-end tests, security tests, etc.

## Preparing the tests

To run the tests, you need to have the following installed:

* Python 3.6 or greater
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)


## Running the Tests

You can run these tests using the following commands from inside the root directory for the project.

```shell
pipenv install
pipenv shell
pytest -m TEST_TYPE --env=TEST_ENV
```

* `TEST_TYPE` is `dist` for `kinto-dist` deployments, `settings` for `kinto-settings` deployments and `webextensions` for `kintowe` deployments
* `TEST_ENV` is one of the environments listed in the `manifest.ini` file.
