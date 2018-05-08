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
    # request that a specific user review it
    client = Client(
        server_url=conf.get(env, "writer_server"),
        auth=(os.getenv("RS_USER_1_LOGIN"), os.getenv("RS_USER_1_PASSWD"))
    )
    data = {"qa": "testing"}
    client.create_collection(id="qatest", if_not_exists=True, bucket="main-workspace")
    cr_response = client.create_record(data=data, collection="qatest", bucket="main-workspace")
    new_record_id = cr_response["data"]["id"]
    changes = JSONPatch(
        [dict(op="add", path="/data/members/0", value="kinto_rs_2")]
    )
    client.patch_group(
        id="qatest-reviewers",
        bucket="main-workspace",
        changes=changes
    )

    # Now request a review of these changes
    client.patch_collection(
        id="qatest",
        bucket="main-workspace",
        data={"status": "to-review"}
    )
    pre_sign_info = client.get_collection(id="qatest", bucket="main-workspace")

    # Create a second client to act as the reviewer and approve the reqqust
    reviewer_client = Client(
        server_url=conf.get(env, "writer_server"),
        auth=(os.getenv("RS_USER_2_LOGIN"), os.getenv("RS_USER_2_PASSWD"))
    )
    reviewer_client.patch_collection(
        id="qatest",
        bucket="main-workspace",
        data={"status": "to-sign"}
    )

    # If last_signature_date has changed, we know the signing successfully happened
    post_sign_info = client.get_collection(id="qatest", bucket="main-workspace")
    assert pre_sign_info["data"]["last_signature_date"] != post_sign_info["data"]["last_signature_date"]

    # Clean up after ourselves
    dr_response = client.delete_record(id=new_record_id, collection="qatest", bucket="main-workspace")
    assert dr_response["deleted"] is True
