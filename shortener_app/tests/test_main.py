import json

import pytest
from fastapi.testclient import TestClient

from shortener_app import main


@pytest.fixture
def api_client():
    app = main.app
    client = TestClient(app)
    yield client


def test_read_root(api_client):
    response = api_client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to the URL shortener API"


def test_create_url(api_client):
    response = api_client.post(
        "/url",
        data=json.dumps({"target_url": "https://www.google.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    assert "url" in response.json().keys()
    assert "admin_url" in response.json().keys()


def test_forward_to_target_url(api_client):
    # First, create a URL
    response = api_client.post(
        "/url",
        data=json.dumps({"target_url": "https://www.google.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    url_info = response.json()

    # Then, forward to the target URL
    api_client.follow_redirects = True
    response = api_client.get(url_info["url"])
    assert response.status_code == 200


def test_get_url_info(api_client):
    # First, create a URL
    response = api_client.post(
        "/url",
        data=json.dumps({"target_url": "https://www.google.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    url_info = response.json()

    # Then, get the URL information
    api_client.follow_redirects = True
    response = api_client.get(url_info["admin_url"])
    assert response.status_code == 200


def test_delete_url(api_client):
    # First, create a URL
    response = api_client.post(
        "/url",
        data=json.dumps({"target_url": "https://www.google.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    url_info = response.json()

    # Then, delete the URL
    response = api_client.delete(url_info["admin_url"])
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["detail"] == (
        "Successfully deleted shortened URL for 'https://www.google.com'"
    )

    # Check that the URL is no longer accessible
    response = api_client.get(url_info["url"])
    assert response.status_code == 404
