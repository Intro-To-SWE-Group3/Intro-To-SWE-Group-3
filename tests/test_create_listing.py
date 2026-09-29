from types import SimpleNamespace
from uuid import UUID

import routes.listings as listings


def test_create_listing_generates_uuid_image_name(client, listing_payload, monkeypatch):
    uploaded = {}
    inserted = {}

    def upload_image(blob_name, image_data):
        uploaded["blob_name"] = blob_name
        uploaded["image_data"] = image_data
        return f"https://blob.test/{blob_name}"

    def insert_listing(*args):
        inserted["args"] = args

    monkeypatch.setattr(
        listings,
        "AzureBlobStorage",
        lambda: SimpleNamespace(upload_image=upload_image),
    )
    monkeypatch.setattr(listings, "insert_listing", insert_listing)

    response = client.post("/listings", json=listing_payload)
    body = response.get_json()

    assert response.status_code == 201
    assert body["image_blob_name"].endswith(".jpg")
    UUID(body["image_blob_name"][:-4])
    assert uploaded["blob_name"] == body["image_blob_name"]
    assert uploaded["image_data"] == b"image-bytes"
    assert inserted["args"][-1] == body["image_blob_name"]


def test_create_listing_returns_uploaded_image_url(client, listing_payload, monkeypatch):
    monkeypatch.setattr(
        listings,
        "AzureBlobStorage",
        lambda: SimpleNamespace(
            upload_image=lambda name, data: "https://blob.test/image.jpg"
        ),
    )
    monkeypatch.setattr(listings, "insert_listing", lambda *args: None)

    response = client.post("/listings", json=listing_payload)

    assert response.status_code == 201
    assert response.get_json()["image_url"] == "https://blob.test/image.jpg"


def test_create_listing_rejects_missing_json(client):
    response = client.post("/listings", data="not-json", content_type="text/plain")

    assert response.status_code == 400
    assert response.get_json()["error"] == "JSON request body is required"


def test_create_listing_rejects_missing_image_data(client, listing_payload):
    listing_payload.pop("image_data")

    response = client.post("/listings", json=listing_payload)

    assert response.status_code == 400
    assert response.get_json()["fields"] == ["image_data"]


def test_create_listing_rejects_invalid_base64(client, listing_payload):
    listing_payload["image_data"] = "not-valid-base64"

    response = client.post("/listings", json=listing_payload)

    assert response.status_code == 400
    assert response.get_json()["error"] == "image_data must be valid Base64"


def test_create_listing_generates_different_names(client, listing_payload, monkeypatch):
    uploaded_names = []

    monkeypatch.setattr(
        listings,
        "AzureBlobStorage",
        lambda: SimpleNamespace(
            upload_image=lambda name, data: uploaded_names.append(name) or "https://blob.test/image.jpg"
        ),
    )
    monkeypatch.setattr(listings, "insert_listing", lambda *args: None)

    first_response = client.post("/listings", json=listing_payload)
    second_response = client.post("/listings", json=listing_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert uploaded_names[0] != uploaded_names[1]
