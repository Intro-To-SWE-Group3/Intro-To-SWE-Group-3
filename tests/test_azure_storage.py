from types import SimpleNamespace

import pytest

import database.azure_storage as storage


def test_azure_storage_uses_azure_configuration(monkeypatch):
    captured = {}
    container = object()
    service = SimpleNamespace(get_container_client=lambda name: container)

    monkeypatch.setenv("AZURE_STORAGE_CONNECTION_STRING", "azure-connection-string")
    monkeypatch.setenv("AZURE_STORAGE_CONTAINER_NAME", "images")

    def from_connection_string(connection_string):
        captured["connection_string"] = connection_string
        return service

    monkeypatch.setattr(
        storage.BlobServiceClient,
        "from_connection_string",
        from_connection_string,
    )

    client = storage.AzureBlobStorage()

    assert captured["connection_string"] == "azure-connection-string"
    assert client.container_client is container


def test_azure_storage_rejects_missing_connection_string(monkeypatch):
    monkeypatch.delenv("AZURE_STORAGE_CONNECTION_STRING", raising=False)
    monkeypatch.setenv("AZURE_STORAGE_CONTAINER_NAME", "images")

    with pytest.raises(ValueError, match="AZURE_STORAGE_CONNECTION_STRING"):
        storage.AzureBlobStorage()


def test_upload_and_delete_image_use_blob_client(monkeypatch):
    blob_calls = {}
    blob_client = SimpleNamespace(
        url="https://blob.test/image.jpg",
        upload_blob=lambda data, overwrite: blob_calls.update(
            upload=(data, overwrite)
        ),
        delete_blob=lambda: blob_calls.update(delete=True),
    )
    container = SimpleNamespace(get_blob_client=lambda name: blob_calls.update(name=name) or blob_client)
    service = SimpleNamespace(get_container_client=lambda name: container)

    monkeypatch.setenv("AZURE_STORAGE_CONNECTION_STRING", "azure-connection-string")
    monkeypatch.setenv("AZURE_STORAGE_CONTAINER_NAME", "images")
    monkeypatch.setattr(
        storage.BlobServiceClient,
        "from_connection_string",
        lambda connection_string: service,
    )

    client = storage.AzureBlobStorage()

    assert client.upload_image("image.jpg", b"data") == "https://blob.test/image.jpg"
    client.delete_image("image.jpg")

    assert blob_calls["name"] == "image.jpg"
    assert blob_calls["upload"] == (b"data", True)
    assert blob_calls["delete"] is True
