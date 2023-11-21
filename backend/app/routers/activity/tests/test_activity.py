from fastapi.testclient import TestClient
from requests_mock import Mocker

from app.config import settings
from app.main import app

client = TestClient(app)
BASE_PATH = "/v1/activity"
HEADERS = {"Authorization": "Bearer TESTING"}
ORGSTATS_URL = "https://scripts.cisco.com/orgstats/api/1/entries"
CISCO_AUTH_URL = "https://scripts.cisco.com/api/v2/auth/login"
TEST_USER_ID = "user_id"
SOURCE = "BDB Task"
SOURCE_URL = "https://example.com"
USER_ACTION = "tool"
DURATION = 10
SR_NUMBER = "612345678"


def test_create_activity(requests_mock: Mocker) -> None:
    """
    Test creating an activity record
    """
    requests_mock.get(CISCO_AUTH_URL, headers={"access_token": "TOKEN"})
    requests_mock.get(ORGSTATS_URL, json=[{"N": "name", "I": "username"}])
    r = client.post(
        BASE_PATH,
        headers=HEADERS,
        json={
            "user_id": TEST_USER_ID,
            "source": SOURCE,
            "source_url": SOURCE_URL,
            "action": USER_ACTION,
            "duration": DURATION,
            "sr": SR_NUMBER,
        },
    )
    assert r.status_code == 200


def test_create_activity_not_found(requests_mock: Mocker) -> None:
    """
    Test creating an activity record
    """
    requests_mock.get(CISCO_AUTH_URL, headers={"access_token": "TOKEN"})
    requests_mock.get(ORGSTATS_URL, json={})
    r = client.post(
        BASE_PATH,
        headers=HEADERS,
        json={
            "user_id": TEST_USER_ID,
            "source": SOURCE,
            "source_url": SOURCE_URL,
            "action": USER_ACTION,
            "duration": DURATION,
            "sr": SR_NUMBER,
        },
    )
    assert r.status_code == 404


def test_get_activity_w_bad_token() -> None:
    """
    Test GEt api with bad token
    """
    r = client.get(
        BASE_PATH,
        headers={"Authorization": "Bearer BAD_TOKEN"},
    )
    assert r.status_code == 401


def test_get_bad_filter() -> None:
    """
    Test Get api with bad filter
    """
    access_token = settings.static_token
    r = client.get(
        BASE_PATH + "?filter=BAD_FILTER",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert r.status_code == 422


def test_get_with_all_params(requests_mock: Mocker) -> None:
    """
    Test get api with all the query params
    """
    requests_mock.get(CISCO_AUTH_URL, headers={"access_token": "TOKEN"})
    requests_mock.get(ORGSTATS_URL, json=[{"N": "name", "I": "username"}])
    # create mock mongodata
    r = client.post(
        BASE_PATH,
        headers=HEADERS,
        json={
            "user_id": TEST_USER_ID,
            "source": SOURCE,
            "source_url": SOURCE_URL,
            "action": USER_ACTION,
            "duration": DURATION,
            "sr": SR_NUMBER,
        },
    )
    assert r.status_code == 200

    access_token = settings.static_token
    limit = 200
    skip = 0
    sort_key = "start_date"
    sort_ascending = False
    # test for all the parmas except filter and projection
    r = client.get(
        BASE_PATH,
        params={
            "limit": limit,
            "skip": skip,
            "sort_key": sort_key,
            "sort_ascending": sort_ascending,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert r.status_code == 200

    # Test for projection param with a json
    r = client.get(
        BASE_PATH,
        params={"projection": "{}"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert r.status_code == 200

    # Test for projection param with valid projections
    r = client.get(
        BASE_PATH,
        params={
            "projection": "id, user_id, source, start_time, end_time, ' \
                'duration, sr, created_date, action"
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert r.status_code == 200


def test_update_unknown_activity() -> None:
    """
    Test update activity record not found
    """

    r = client.put(f"{BASE_PATH}/63ef7c778367b25225e9ffa1", headers=HEADERS)
    assert r.status_code == 404


def test_lifecycle_activity(requests_mock: Mocker) -> None:
    """
    Test activity
    """
    requests_mock.get(CISCO_AUTH_URL, headers={"access_token": "TOKEN"})
    requests_mock.get(ORGSTATS_URL, json=[{"N": "name", "I": "username"}])
    r = client.post(
        BASE_PATH,
        headers=HEADERS,
        json={
            "user_id": TEST_USER_ID,
            "source": SOURCE,
            "source_url": SOURCE_URL,
            "action": USER_ACTION,
            "duration": DURATION,
            "sr": SR_NUMBER,
        },
    )
    assert r.status_code == 200
    result = r.json()
    activity_id = result.get("id")

    r = client.put(f"{BASE_PATH}/{activity_id}", headers=HEADERS)
    assert r.status_code == 200
