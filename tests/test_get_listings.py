import routes.listings as listings


def test_get_listings_returns_database_rows(client, monkeypatch):
    rows = [
        {"Item_Name": "Test book", "Item_Price": 10},
        {"Item_Name": "Test notes", "Item_Price": 5},
    ]
    monkeypatch.setattr(listings, "get_all_listings", lambda: rows)

    response = client.get("/listings")

    assert response.status_code == 200
    assert response.get_json() == rows
