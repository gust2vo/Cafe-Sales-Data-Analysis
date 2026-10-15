
import os
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def create_database_engine():
    server = os.getenv("MSSQL_SERVER")
    port = os.getenv("MSSQL_PORT", "1433")
    database = os.getenv("MSSQL_DATABASE")
    user = os.getenv("MSSQL_USER")
    password = os.getenv("MSSQL_PASSWORD")

    required_values = {
        "MSSQL_SERVER": server,
        "MSSQL_DATABASE": database,
        "MSSQL_USER": user,
        "MSSQL_PASSWORD": password,
    }

    missing_values = [
        name
        for name, value in required_values.items()
        if not value
    ]

    if missing_values:
        raise ValueError(
            "Variáveis ausentes no .env: "
            + ", ".join(missing_values)
        )

    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "TrustServerCertificate=yes;"
    )

    connection_url = (
        "mssql+pyodbc:///?odbc_connect="
        + quote_plus(connection_string)
    )

    return create_engine(connection_url)


def load_data(engine) -> pd.DataFrame:
    query = text(
        "SELECT * FROM staging.cafe_sales_raw"
    )

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    if df.empty:
        raise ValueError(
            "A tabela staging.cafe_sales_raw não retornou dados."
        )

    return df
