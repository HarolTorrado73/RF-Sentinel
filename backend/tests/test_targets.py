from fastapi.testclient import TestClient


def test_target_crud_flow(client: TestClient, auth_headers: dict[str, str]) -> None:
    create_response = client.post(
        "/api/v1/targets/",
        json={
            "name": "Localhost",
            "target_type": "ip",
            "value": "127.0.0.1",
            "description": "Test target",
        },
        headers=auth_headers,
    )
    assert create_response.status_code == 200
    target = create_response.json()
    assert target["name"] == "Localhost"

    list_response = client.get("/api/v1/targets/", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    target_id = target["id"]
    get_response = client.get(f"/api/v1/targets/{target_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == target_id

    delete_response = client.delete(f"/api/v1/targets/{target_id}", headers=auth_headers)
    assert delete_response.status_code == 200

    list_after_delete = client.get("/api/v1/targets/", headers=auth_headers)
    assert list_after_delete.status_code == 200
    assert list_after_delete.json() == []
