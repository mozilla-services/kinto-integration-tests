import os
import pytest

from kinto_http import Client
from kinto_http.patch_type import JSONPatch


@pytest.mark.settings
@pytest.mark.skipif(
    pytest.config.getoption("env") != "stage",
    reason="Test only runs on staging"
)
def test_create_collection_in_main_bucket(conf, env):
    # Create a record inside the 'main-workspace' bucket and then
    # PATCH the collection to say someone else can review it
    collection = "qatest"
    client = Client(
        server_url=conf.get(env, "writer_server"),
        auth=(os.getenv("RS_USER_1_LOGIN"), os.getenv("RS_USER_1_PASSWD")),
        bucket="main-workspace"
    )
    client.create_collection(id=collection, if_not_exists=True)
    changes = JSONPatch(
        [dict(op="add", path="/data/members/0", value=os.getenv("RS_USER_2_LOGIN"))]
    )
    client.patch_group(
        id="{0}-reviewers".format(collection),
        changes=changes
    )
    data = {"qa": "testing"}
    cr_response = client.create_record(data=data, collection=collection)
    new_record_id = cr_response["data"]["id"]
    assert new_record_id is not False

    # Now request a review of these changes
    client.patch_collection(
        id=collection,
        data={"status": "to-review"}
    )
    pre_sign_info = client.get_collection(id=collection)

    # Create a second client to act as the reviewer and approve the request
    reviewer_client = Client(
        server_url=conf.get(env, "writer_server"),
        auth=(os.getenv("RS_USER_2_LOGIN"), os.getenv("RS_USER_2_PASSWD")),
        bucket="main-workspace"
    )
    reviewer_client.patch_collection(
        id=collection,
        data={"status": "to-sign"}
    )

    # If last_signature_date has changed, we know the signing successfully happened
    post_sign_info = client.get_collection(id=collection)
    assert pre_sign_info["data"]["last_signature_date"] != post_sign_info["data"]["last_signature_date"]

    # Clean up after ourselves
    dr_response = client.delete_record(id=new_record_id, collection=collection)
    assert dr_response["deleted"] is True
    client.patch_collection(
        id=collection,
        data={"status": "to-review"}
    )
    reviewer_client.patch_collection(
        id=collection,
        data={"status": "to-sign"}
    )
