from fastapi.testclient import TestClient


class _FakeHost:
    def state(self) -> str:
        return "up"

    def all_protocols(self) -> list[str]:
        return ["tcp"]

    def __getitem__(self, protocol: str) -> dict[int, dict[str, str]]:
        if protocol != "tcp":
            return {}
        return {
            80: {
                "state": "open",
                "name": "http",
                "product": "nginx",
                "version": "1.25",
            }
        }


class _FakeScanner:
    def __init__(self) -> None:
        self._hosts: list[str] = []

    def scan(self, hosts: str, arguments: str) -> None:  # noqa: ARG002
        self._hosts = [hosts]

    def all_hosts(self) -> list[str]:
        return self._hosts

    def __getitem__(self, host: str) -> _FakeHost:  # noqa: ARG002
        return _FakeHost()


def test_scan_flow(client: TestClient, auth_headers: dict[str, str], monkeypatch) -> None:
    create_target = client.post(
        "/api/v1/targets/",
        json={
            "name": "Scan Target",
            "target_type": "ip",
            "value": "127.0.0.1",
            "description": "Target for scan",
        },
        headers=auth_headers,
    )
    target_id = create_target.json()["id"]

    create_scan = client.post(
        "/api/v1/scans/",
        json={"target_id": target_id, "scan_type": "ping"},
        headers=auth_headers,
    )
    assert create_scan.status_code == 200
    scan = create_scan.json()
    scan_id = scan["id"]

    list_scans = client.get("/api/v1/scans/", headers=auth_headers)
    assert list_scans.status_code == 200
    assert len(list_scans.json()) == 1

    get_scan = client.get(f"/api/v1/scans/{scan_id}", headers=auth_headers)
    assert get_scan.status_code == 200
    assert get_scan.json()["id"] == scan_id

    monkeypatch.setattr("app.services.scan.nmap.PortScanner", _FakeScanner)
    execute_scan = client.post(f"/api/v1/scans/{scan_id}/execute", headers=auth_headers)

    assert execute_scan.status_code == 200
    executed_payload = execute_scan.json()
    assert executed_payload["status"] == "completed"
    assert executed_payload["results"]["hosts"][0]["ip"] == "127.0.0.1"
