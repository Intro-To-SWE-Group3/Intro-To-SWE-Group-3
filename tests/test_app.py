import app as application


def test_homepage_blueprint_is_registered(client):
    assert "homepage" in application.app.blueprints

    response = client.get("/")

    assert response.status_code == 200
    assert b"<html" in response.data.lower()


def test_cors_allows_cross_origin_requests(client):
    response = client.get("/", headers={"Origin": "https://example.com"})

    assert response.headers["Access-Control-Allow-Origin"] == "https://example.com"
