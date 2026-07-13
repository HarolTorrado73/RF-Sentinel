from pathlib import Path

from fastapi.testclient import TestClient


def test_report_flow(
    client: TestClient,
    auth_headers: dict[str, str],
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr("app.services.report.ReportService.REPORTS_DIR", str(tmp_path))

    target_response = client.post(
        "/api/v1/targets/",
        json={
            "name": "Report Target",
            "target_type": "ip",
            "value": "127.0.0.1",
            "description": "Target for report",
        },
        headers=auth_headers,
    )
    target_id = target_response.json()["id"]

    scan_response = client.post(
        "/api/v1/scans/",
        json={"target_id": target_id, "scan_type": "ping"},
        headers=auth_headers,
    )
    scan_id = scan_response.json()["id"]

    create_report = client.post(
        "/api/v1/reports/",
        json={"scan_id": scan_id, "title": "Daily Report", "report_type": "json"},
        headers=auth_headers,
    )
    assert create_report.status_code == 200
    report = create_report.json()
    report_id = report["id"]

    list_reports = client.get("/api/v1/reports/", headers=auth_headers)
    assert list_reports.status_code == 200
    assert len(list_reports.json()) == 1

    get_report = client.get(f"/api/v1/reports/{report_id}", headers=auth_headers)
    assert get_report.status_code == 200

    generate_report = client.post(
        f"/api/v1/reports/{report_id}/generate",
        headers=auth_headers,
    )
    assert generate_report.status_code == 200

    report_file_path = generate_report.json()["file_path"]
    assert Path(report_file_path).exists()

    download_report = client.get(
        f"/api/v1/reports/{report_id}/download",
        headers=auth_headers,
    )
    assert download_report.status_code == 200

    delete_report = client.delete(f"/api/v1/reports/{report_id}", headers=auth_headers)
    assert delete_report.status_code == 200
