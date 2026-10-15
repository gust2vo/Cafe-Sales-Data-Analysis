import pandas as pd

def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    new_columns_names = {
        "Transaction ID": "transaction_id",
        "Item": "item",
        "Quantity": "quantity",
        "Price Per Unit": "price_per_unit",
        "Total Spent": "total_spent",
        "Payment Method": "payment_method",
        "Location": "location",
        "Transaction Date": "transaction_date",
    }

    df = df.rename(columns=new_columns_names)

    expected_columns = list(new_columns_names.values())
    missing_columns = [
        column
        for column in expected_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Colunas esperadas não encontradas: "
            + ", ".join(missing_columns)
        )

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    df["transaction_date_raw"] = df["transaction_date"]
    df["quantity_raw"] = df["quantity"]
    df["price_per_unit_raw"] = df["price_per_unit"]
    df["total_spent_raw"] = df["total_spent"]

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    ).astype("Int64")

    df["price_per_unit"] = pd.to_numeric(
        df["price_per_unit"],
        errors="coerce"
    )

    df["total_spent"] = pd.to_numeric(
        df["total_spent"],
        errors="coerce"
    )

    return df
