# Summary
Tests for the Kinto server fall into 3 categories:

1. unit tests - located here: https://github.com/Kinto/kinto/tests
2. loadtests - located here:  https://github.com/Kinto/kinto-loadtests
3. configuration check tests - located in this repo

This repo is a clearinghouse for all automated tests that don't need to reside in their own repository.
They would include a variety of test types that usually fall in the middle of the test pyramid:
API tests, config and URL checks, deployment tests, end-2-end tests, security tests, etc.

## Preparing the tests

Building the image for running tests requires you to have
[Docker](https://www.docker.com/) installed:

```shell
docker build -t kinto-integration-tests .
```

## Running the Tests

You can run these tests using the following command:

```shell
docker run kinto-integration-tests pytest --env=TEST_ENV config-test/
```

Where `TEST_ENV` is one of the environments listed in the `manifest.ini` file.
