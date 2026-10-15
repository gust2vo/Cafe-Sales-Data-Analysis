
import pandas as pd

from validate import (
    VALID_ITEMS,
    VALID_LOCATIONS,
    VALID_PAYMENT_METHODS,
    PRICES_ITEM
)

def prepare_data_for_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "item_raw" not in df.columns:
        df["item_raw"] = df["item"]

    if "location_raw" not in df.columns:
        df["location_raw"] = df["location"]

    if "payment_method_raw" not in df.columns:
        df["payment_method_raw"] = df["payment_method"]

    df.loc[~df["item"].isin(VALID_ITEMS), "item"] = pd.NA
    df.loc[~df["location"].isin(VALID_LOCATIONS), "location"] = pd.NA
    df.loc[
        ~df["payment_method"].isin(VALID_PAYMENT_METHODS),
        "payment_method"
    ] = pd.NA

    df.loc[
        df["quantity"].notna() & df["quantity"].le(0),
        "quantity"
    ] = pd.NA

    df.loc[
        df["price_per_unit"].notna() & df["price_per_unit"].le(0),
        "price_per_unit"
    ] = float("nan")

    df.loc[
        df["total_spent"].notna() & df["total_spent"].le(0),
        "total_spent"
    ] = float("nan")

    return df


def clean_item(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    mask_item_na = (
      df['item'].isna() &
      (df['price_per_unit'].isin(PRICES_ITEM))
    )
    
    df.loc[mask_item_na, 'item'] = (
      df.loc[mask_item_na, 'price_per_unit'].map(PRICES_ITEM)
    )
    
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = prepare_data_for_cleaning(df)

    df = clean_item(df)

    return df
