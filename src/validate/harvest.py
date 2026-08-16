import pandas as pd

from src.extract.harvest import load_raw_harvest
from src.transform.harvest import transform_harvest

def add_reason(df, mask, reason):
    df.loc[
        mask,
        "validation_reason"
    ] = df.loc[
        mask,
        "validation_reason"
    ].apply(
        lambda x: f"{x};{reason}" if x else reason
    )

def validate_harvest(df):
    df = df.copy()

    df["validation_status"] = "OK"
    df["validation_reason"] = ""

    duplicate_mask = df["harvest_id"].duplicated(
        keep=False
    )

    df.loc[
        duplicate_mask,
        "validation_status"
    ] = "ERROR"

    add_reason(
        df,
        duplicate_mask,
        "duplicate_harvest_id"
     )

    unknown_crop_mask = df["crop_name"].isna()

    df.loc[
        unknown_crop_mask,
        "validation_status"
    ] = "ERROR"

    add_reason(
        df,
        unknown_crop_mask,
        "unknown_crop"
    )

    unknown_farm_mask = df["farm_id"].isna()

    df.loc[
        unknown_farm_mask,
        "validation_status"
    ] = "ERROR"

    add_reason(
        df,
        unknown_farm_mask,
        "unknown_farm"
    )

    unknown_client_mask = df["client_id"].isna()

    df.loc[
        unknown_client_mask,
        "validation_status"
    ] = "ERROR"

    add_reason(
        df,
        unknown_client_mask,
        "unknown_client"
    )

    today = pd.Timestamp.today().normalize()

    future_date_mask = (
        df["harvest_date"].notna()
        & (df["harvest_date"] > today)
    )

    df.loc[
        future_date_mask,
        "validation_status"
    ] = "ERROR"

    add_reason(
        df,
        future_date_mask,
        "future_date"
    )

    invalid_date_mask = df["harvest_date"].isna()

    df.loc[
        invalid_date_mask,
        "validation_status"
    ] = "ERROR"

    add_reason(
        df,
        invalid_date_mask,
        "invalid_date"
    )

    invalid_quantity_mask = (
        df["quantity_g"].isna()
        | (df["quantity_g"] <= 0)
    )

    df.loc[
        invalid_quantity_mask,
        "validation_status"
    ] = "ERROR"

    add_reason(
        df,
        invalid_quantity_mask,
        "invalid_quantity"
    )
    
    possible_duplicate_mask = df.duplicated(
        subset=[
            "farm_id",
            "house_id",
            "harvest_date",
            "client_id",
            "crop_name",
            "quantity_g",
        ],
        keep=False
    )

    possible_duplicate_mask = (
        possible_duplicate_mask
        & (df["validation_status"] == "OK")
    )

    unusual_quantity_mask = (
        df["quantity_g"].notna()
        & (df["quantity_g"] >= 5000)
        & (df["validation_status"] == "OK")
    )

    df.loc[
        possible_duplicate_mask,
        "validation_status"
    ] = "WARNING"

    add_reason(
        df,
        possible_duplicate_mask,
        "possible_duplicate"
    )

    df.loc[
        unusual_quantity_mask,
        "validation_status"
    ] = "WARNING"

    add_reason(
        df,
        unusual_quantity_mask,
        "unusual_quantity"
    )
    return df

def main():
    harvest = load_raw_harvest()
    transformed = transform_harvest(harvest)
    validated = validate_harvest(transformed)

    print(
        validated[
            [
                "harvest_id",
                "harvest_date",
                "validation_status",
                "validation_reason",
            ]
        ]
    )

if __name__ == "__main__":
   main()
