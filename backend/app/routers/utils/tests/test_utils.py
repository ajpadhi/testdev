from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_status() -> None:
    """
    Test API status
    """
    # get Status
    r = client.get("/v1/utils/api-status")
    assert r.status_code == 200
