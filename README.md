#Summary#
Tests for the Kinto server fall into 3 categories:
1. unit tests - located here: https://github.com/Kinto/kinto/tests
2. loadtests - located here:  https://github.com/Kinto/kinto-loadtests
3. configuration check tests - located in this repo

This repo is a clearinghouse for all automated tests that don't need to reside in their own repository.
They would include a variety of test types that usually fall in the middle of the test pyramid:
API tests, config and URL checks, deployment tests, end-2-end tests, security tests, etc.

These tests can all be run at a go using the "run" file or executed via a Docker container.

###General Configuration###

Python 3.5.2 or greater is required.

It's highly recommended to use [Virtualenv](https://virtualenv.pypa.io/en/latest/)
in order to have an isolated environment.

From this directory

1. virtualenv . -p /path/to/python
2. ./bin/pip install -r dev-requirements.txt

#Run Tests#


#TestRail Integration#
####Creating TestRail-aware Tests####

Tests that you want to report results to TestRail need to make sure that they
are importing the TestRail py.test plugin:

_from pytest_testrail.plugin import testrail_

Then you need to add a decorator to a test in order for the plugin to report
the results of the test. Here'a sample:

_@testrail('C5475')_

The value 'C5475' is the ID that TestRail assigned to the case you are testing,
which can be obtained via the TestRail admin. Without the decorator the test
will still run but no results will be reported to TestRail.


####Running The Tests####

To run the tests, do the following

1. Copy _config-check-test/testrail.cfg-dist_ to _config-check-test/testrail.cfg_ and add your TestRail user name and password to the configuration file
2. Make sure you are connected to the Mozilla VPN
3. Run the tests using _py.test --env=<ENVIRONMENT> --testrail=config-check-test/testrail.cfg config-check-test/_ where <ENVIRONMENT> is _stage_ or _prod_

If you get an error message similar to:

_INTERNALERROR> requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:645)_

then add _--no-ssl-cert-check_ as a parameter to the command used in step 3.

These configuration check tests are currently only being run against staging
instances of Kinto.
