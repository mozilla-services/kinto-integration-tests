import pytest
import requests
from random import randint


@pytest.mark.settings
def test_email_notifications_work(env, conf, qauser, qapasswd, request):
    if request.config.getoption('env') != 'stage':
        pytest.skip('Test only runs on STAGE')

    url = conf.get(env, 'qa_collection_url')
    auth = (qauser, qapasswd)

    # Add record to QA collection
    data = {'data': {'qa': randint(1, 99999)}}
    resp = requests.post(
        json=data,
        auth=auth,
        url=url + '/records'
    )
    assert resp.status_code == 201

    # Ask for a review
    data = {'data': {'status': 'to-review'}}
    resp = requests.patch(
        json=data,
        auth=auth,
        url=url
    )
    assert resp.status_code == 200

    # Look for the email that has the message that a review has been requested
    resp = requests.get(url="https://restmail.net/mail/kintoemailer")
    emails = resp.json()

    # The email with the review message is always the first one
    email = emails[0]
    assert email['text'] == "For QA purposes :)\n"
