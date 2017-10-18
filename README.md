# Summary
Tests for the Kinto server fall into 3 categories:

1. unit tests - located here: https://github.com/Kinto/kinto/tests
2. loadtests - located here:  https://github.com/Kinto/kinto-loadtests
3. configuration check tests - located in this repo

This repo is a clearinghouse for all automated tests that don't need to reside in their own repository.
They would include a variety of test types that usually fall in the middle of the test pyramid:
API tests, config and URL checks, deployment tests, end-2-end tests, security tests, etc.

These tests can all be run at a go using the "run" file or executed via a Docker container.

### General Configuration

These are the minimum requirements:

* Python 3.5.2 or greater
* [Tox](https://tox.readthedocs.io/en/latest/)


# Running Configuration Check Tests

#### Running The Tests

Tests are run using tox. First, we need to set an environment variable called TEST_ENV to be the environment we want our tests to run under. Check the documentation for your shell to determine how to do so.

* dev
* prod
* stage

These match the environments listed in our _manifest.ini_ file.

Then just use the command _tox_ to run the tests.
