# Summary
Tests for the Kinto server fall into 3 categories:

1. unit tests - located here: https://github.com/Kinto/kinto/tests
2. loadtests - located here:  https://github.com/Kinto/kinto-loadtests
3. configuration check tests - located in this repo

This repo is a clearinghouse for all automated tests that don't need to reside in their own repository.
They would include a variety of test types that usually fall in the middle of the test pyramid:
API tests, config and URL checks, deployment tests, end-2-end tests, security tests, etc.

These tests can all be run at a go using the "run" file or executed via a Docker container.

## General Configuration

These are the minimum requirements:

* Python 3.5.2 or greater

### Installing Dependencies via Virtualenv and Pip

You can install all the dependencies for running these tests locally by installing:

* pip (https://pip.readthedocs.io/en/stable/)
* virtualenv (https://virtualenv.pypa.io/en/stable/)

Please follow the instructions on how to install those tools and then do the following:

* create a virtual environment using the minimum recommended version of Python
* activate the virtual environment
* install the required dependencies using `pip install -r requirements.txt`


### Installing Dependencies via Pipenv

Pipenv (https://docs.pipenv.org/) can also be used to install the required dependencies.
Please consult the documentation for the project for instructions on installing it.

Once you've installed Pipenv, you can do the following:

* create the virtual environment and install dependencies using `pipenv install`
* activate the virtual environment using `pipenv shell`


## Running The Tests

You can run these tests using `pytest --env=TEST_ENV config-tests/` where `TEST_ENV`
is one of the environments listed in the `manifest.ini` file.


