# database/db.py
# Handles the connection between the Flask backend and the SQL database.
# Provides reusable database connection functionality so routes and
# services do not need to repeat database connection code.

import os
import pyodbc

def get_db_connection():
    """
    Establish a connection to the SQL database.
    Returns a database connection object.
    """
    server = os.getenv("SQL_SERVER_NAME", "").strip()
    database = os.getenv("SQL_DATABASE_NAME", "").strip()
    username = os.getenv("SQL_USERNAME", "").strip()
    password = os.getenv("SQL_PASSWORD", "")
    driver = os.getenv("DRIVER", "ODBC Driver 17 for SQL Server").strip("{} ")
    if not all((server, database, username, password)):
        raise RuntimeError("SQL database environment variables are not fully configured")

    connection_string = (
        f"DRIVER={{{driver}}};SERVER={server};PORT=1433;"
        f"DATABASE={database};UID={username};PWD={password}"
    )

    return pyodbc.connect(connection_string)