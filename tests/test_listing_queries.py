from types import SimpleNamespace

import database.queries.listing as queries


def test_insert_listing_executes_and_commits(monkeypatch):
    executed = {}
    state = {"committed": False, "cursor_closed": False, "connection_closed": False}

    cursor = SimpleNamespace(
        execute=lambda statement, parameters: executed.update(
            statement=statement, parameters=parameters
        ),
        close=lambda: state.update(cursor_closed=True),
    )
    connection = SimpleNamespace(
        cursor=lambda: cursor,
        commit=lambda: state.update(committed=True),
        close=lambda: state.update(connection_closed=True),
    )
    monkeypatch.setattr(queries, "get_db_connection", lambda: connection)

    queries.insert_listing(
        "Test book",
        "Test description",
        10,
        "Book",
        2,
        "https://blob.test/image.jpg",
        "image.jpg",
    )

    assert executed["statement"].count("?") == 7
    assert executed["parameters"] == (
        "Test book",
        "Test description",
        10,
        "Book",
        2,
        "https://blob.test/image.jpg",
        "image.jpg",
    )
    assert state == {
        "committed": True,
        "cursor_closed": True,
        "connection_closed": True,
    }


def test_get_all_listings_maps_columns_to_rows(monkeypatch):
    state = {"cursor_closed": False, "connection_closed": False}
    cursor = SimpleNamespace(
        description=[("Item_Name",), ("Item_Price",)],
        execute=lambda statement: None,
        fetchall=lambda: [("Test book", 10), ("Test notes", 5)],
        close=lambda: state.update(cursor_closed=True),
    )
    connection = SimpleNamespace(
        cursor=lambda: cursor,
        close=lambda: state.update(connection_closed=True),
    )
    monkeypatch.setattr(queries, "get_db_connection", lambda: connection)

    listings = queries.get_all_listings()

    assert listings == [
        {"Item_Name": "Test book", "Item_Price": 10},
        {"Item_Name": "Test notes", "Item_Price": 5},
    ]
    assert state == {"cursor_closed": True, "connection_closed": True}
