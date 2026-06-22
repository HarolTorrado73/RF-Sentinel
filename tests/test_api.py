import pytest
from httpx import ASGITransport, AsyncClient

from rf_sentinel.api.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_scan_validation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/scan", json={"start_frequency": 1000, "stop_frequency": 500})
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_start_scan():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/scan", json={"start_frequency": 100e6, "stop_frequency": 200e6, "step": 1e6}
        )
        assert response.status_code == 200
        data = response.json()
        assert "scan_id" in data
        assert data["status"] == "running"


@pytest.mark.asyncio
async def test_detect_signals():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/detect", params={"capture_id": 1})
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_capture():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/capture", params={"frequency": 433.92e6, "duration": 10.0})
        assert response.status_code == 200
        data = response.json()
        assert "center_frequency" in data


@pytest.mark.asyncio
async def test_export_pdf():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/export/pdf", params={"capture_id": 1})
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_export_json():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/export/json", params={"capture_id": 1})
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
