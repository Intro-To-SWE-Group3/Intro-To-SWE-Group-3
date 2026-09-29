from types import SimpleNamespace

import pytest

import database.db as database


def test_get_db_connection_builds_sql_connection_string(monkeypatch):
    captured = {}
    expected_connection = object()

    monkeypatch.setenv("SQL_SERVER_NAME", "sql.example.test")
    monkeypatch.setenv("SQL_DATABASE_NAME", "marketplace")
    monkeypatch.setenv("SQL_USERNAME", "test-user")
    monkeypatch.setenv("SQL_PASSWORD", "test-password")
    monkeypatch.setenv("DRIVER", "{ODBC Driver 17 for SQL Server}")

    def connect(connection_string):
        captured["connection_string"] = connection_string
        return expected_connection

    monkeypatch.setattr(database.pyodbc, "connect", connect)

    assert database.get_db_connection() is expected_connection
    assert captured["connection_string"] == (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=sql.example.test;PORT=1433;"
        "DATABASE=marketplace;UID=test-user;PWD=test-password"
    )


def test_get_db_connection_rejects_missing_sql_configuration(monkeypatch):
    for name in ("SQL_SERVER_NAME", "SQL_DATABASE_NAME", "SQL_USERNAME", "SQL_PASSWORD"):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(RuntimeError, match="not fully configured"):
        database.get_db_connection()
