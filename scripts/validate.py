import pandas as pd

VALID_ITEMS = [
    "Coffee",
    "Tea",
    "Sandwich",
    "Salad",
    "Cake",
    "Cookie",
    "Smoothie",
    "Juice",
]

VALID_LOCATIONS = [
    "Takeaway",
    "In-store",
]

VALID_PAYMENT_METHODS = [
    "Digital Wallet",
    "Credit Card",
    "Cash",
]

ITEM_PRICES = {
    "Coffee": 2.0,
    "Tea": 1.5,
    "Sandwich": 4.0,
    "Salad": 5.0,
    "Cake": 3.0,
    "Cookie": 1.0,
    "Smoothie": 4.0,
    "Juice": 3.0,
}

PRICES_ITEM = {
    2.0: "Coffee",
    1.5: "Tea",
    5.0: "Salad",
    1.0: "Cookie" 
}

""" VALIDAÇÃO DO ID DA TRANSAÇÃO """

def validate_id(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    transaction_id = df["transaction_id"]

    df["transaction_id_validation"] = (
        transaction_id.notna()
        & transaction_id.ne("")
        & transaction_id.duplicated(keep=False).eq(False)
    )

    return df

""" VALIDAÇÃO DAS DATAS """

def validate_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["transaction_date_validation"] = (
        df["transaction_date"].notna()
    )

    return df

""" VALIDAÇÃO DA QUANTIDADE """

def validate_quantity(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["quantity_validation"] = (
        df["quantity"].notna()
        & (df["quantity"] > 0)
    )

    return df


""" VALIDAÇÃO DO PREÇO UNITÁRIO """

def validate_price(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["price_per_unit_validation"] = (
        df["price_per_unit"].notna()
        & (df["price_per_unit"] > 0)
    )

    return df

""" VALIDAÇÃO DO TOTAL GASTO """

def validate_total_spent(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["total_spent_validation"] = (
        df["total_spent"].notna()
        & (df["total_spent"] > 0)
    )

    return df

""" VALIDAÇÃO CRUZADA DO TOTAL GASTO """

def validate_cross_total_spent(
    df: pd.DataFrame,
) -> pd.DataFrame:
    df = df.copy()

    valid_inputs = (
        df["quantity"].notna()
        & (df["quantity"] > 0)
        & df["price_per_unit"].notna()
        & (df["price_per_unit"] > 0)
        & df["total_spent"].notna()
        & (df["total_spent"] > 0)
    )

    expected_total = (
        df["quantity"] * df["price_per_unit"]
    )

    is_consistent = pd.Series(
        pd.NA,
        index=df.index,
        dtype="boolean",
    )

    is_consistent.loc[valid_inputs] = (
        (
            df.loc[valid_inputs, "total_spent"]
            - expected_total.loc[valid_inputs]
        ).abs()
        < 0.05
    )

    df["cross_validation_total_spent"] = is_consistent

    return df

""" VALIDAÇÃO DO ITEM """

def validate_item(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["item_validation"] = (
        df["item"].isin(VALID_ITEMS)
    )

    return df

""" VALIDAÇÃO DA LOCALIZAÇÃO """

def validate_location(
    df: pd.DataFrame,
) -> pd.DataFrame:
    df = df.copy()

    df["location_validation"] = (
        df["location"].isin(VALID_LOCATIONS)
    )

    return df

""" VALIDAÇÃO DO MÉTODO DE PAGAMENTO """

def validate_payment_method(
    df: pd.DataFrame,
) -> pd.DataFrame:
    df = df.copy()

    df["payment_method_validation"] = (
        df["payment_method"].isin(
            VALID_PAYMENT_METHODS
        )
    )

    return df

""" VALIDAÇÃO DA RELAÇÃO ENTRE ITEM E PREÇO """

def validate_item_price(
    df: pd.DataFrame,
) -> pd.DataFrame:
    df = df.copy()

    expected_price = df["item"].map(ITEM_PRICES)

    valid_inputs = (
        expected_price.notna()
        & df["price_per_unit"].notna()
        & (df["price_per_unit"] > 0)
    )

    is_consistent = pd.Series(
        pd.NA,
        index=df.index,
        dtype="boolean",
    )

    is_consistent.loc[valid_inputs] = (
        (
            df.loc[valid_inputs, "price_per_unit"]
            - expected_price.loc[valid_inputs]
        ).abs()
        < 0.05
    )

    df["validation_item_price"] = is_consistent

    return df

""" EXECUTAR TODAS AS VALIDAÇÕES """

VALIDATION_COLUMNS = [
    "transaction_id_validation",
    "transaction_date_validation",
    "quantity_validation",
    "price_per_unit_validation",
    "total_spent_validation",
    "item_validation",
    "location_validation",
    "payment_method_validation",
    "cross_validation_total_spent",
    "validation_item_price",
]

def run_validations(
    df: pd.DataFrame,
) -> pd.DataFrame:
    df = df.copy()

    validation_functions = [
        validate_id,
        validate_dates,
        validate_quantity,
        validate_price,
        validate_total_spent,
        validate_cross_total_spent,
        validate_item,
        validate_location,
        validate_payment_method,
        validate_item_price,
    ]

    for validation_function in validation_functions:
        df = validation_function(df)

    return df

""" RESUMO DAS VALIDAÇÕES """

def summarize_validations(
    df: pd.DataFrame,
    validation_columns: list[str] = VALIDATION_COLUMNS,
) -> pd.DataFrame:

    results = []

    for column in validation_columns:
        results.append({
            "validation": column,
            "valid": int(df[column].eq(True).sum()),
            "invalid": int(df[column].eq(False).sum()),
            "no_result": int(df[column].isna().sum()),
        })

    return pd.DataFrame(results)