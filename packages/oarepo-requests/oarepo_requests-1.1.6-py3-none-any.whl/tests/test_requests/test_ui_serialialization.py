import copy

from thesis.records.api import ThesisDraft, ThesisRecord

from .utils import is_valid_subdict, link_api2testclient


def test_publish(
    client_logged_as,
    users,
    urls,
    publish_request_data_function,
    ui_serialization_result,
    search_clear,
):
    creator_client = client_logged_as(users[0].email)

    receiver = users[1]

    draft1 = creator_client.post(urls["BASE_URL"], json={})
    draft_id = draft1.json["id"]
    ThesisRecord.index.refresh()
    ThesisDraft.index.refresh()

    resp_request_create = creator_client.post(
        urls["BASE_URL_REQUESTS"],
        json=publish_request_data_function(draft1.json["id"]),
    )

    resp_request_submit = creator_client.post(
        link_api2testclient(resp_request_create.json["links"]["actions"]["submit"])
    )
    receiver_client = client_logged_as(users[1].email)
    record = receiver_client.get(f"{urls['BASE_URL']}{draft_id}/draft").json
    ui_record = receiver_client.get(
        f"{urls['BASE_URL']}{draft_id}/draft",
        headers={"Accept": "application/vnd.inveniordm.v1+json"},
    ).json

    assert is_valid_subdict(
        ui_serialization_result(draft_id, ui_record["requests"][0]["id"]),
        ui_record["requests"][0],
    )


def test_resolver_fallback(
    app,
    client_logged_as,
    users,
    urls,
    publish_request_data_function,
    ui_serialization_result,
    search_clear,
):
    creator_client = client_logged_as(users[0].email)
    config_restore = copy.deepcopy(app.config["ENTITY_REFERENCE_UI_RESOLVERS"])
    app.config["ENTITY_REFERENCE_UI_RESOLVERS"] = {}

    receiver = users[1]

    draft1 = creator_client.post(urls["BASE_URL"], json={})
    draft_id = draft1.json["id"]
    ThesisRecord.index.refresh()
    ThesisDraft.index.refresh()

    resp_request_create = creator_client.post(
        urls["BASE_URL_REQUESTS"],
        json=publish_request_data_function(draft1.json["id"]),
    )

    resp_request_submit = creator_client.post(
        link_api2testclient(resp_request_create.json["links"]["actions"]["submit"])
    )
    receiver_client = client_logged_as(users[1].email)
    ui_record = receiver_client.get(
        f"{urls['BASE_URL']}{draft_id}/draft",
        headers={"Accept": "application/vnd.inveniordm.v1+json"},
    ).json
    expected_result = ui_serialization_result(draft_id, ui_record["requests"][0]["id"])
    expected_result["receiver"][
        "label"
    ] = f"id: {users[1].id}"  # the user resolver uses name or email as label, the fallback doesn't know what to use
    assert is_valid_subdict(
        expected_result,
        ui_record["requests"][0],
    )
    app.config["ENTITY_REFERENCE_UI_RESOLVERS"] = config_restore
