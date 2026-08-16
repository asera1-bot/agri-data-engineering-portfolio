import re
import unicodedata
import pandas as pd

from src.extract.harvest import load_raw_harvest

def norm_text(rows):
    if pd.isna(rows):
        return ""

    rows = str(rows)
    rows = unicodedata.normalize("NFKC", rows)
    rows = rows.strip()
    rows = re.sub(r"\s+", "", rows)

    return rows

def transform_harvest(rows):
    df = pd.DataFrame(rows)
    
    text_columns = [
        "farm_raw",
        "house_id",
        "harvest_date",
        "client_raw",
        "crop_raw",
        "quantity_g",
    ]

    for column in text_columns:
        df[column] = df[column].map(norm_text)

    df["house_id"] = df["house_id"].str.upper()

    df["harvest_date"] = pd.to_datetime(
        df["harvest_date"],
        errors="coerce"
    )

    df['quantity_g'] = pd.to_numeric(df['quantity_g'], errors='coerce')

    df['harvest_id'] = pd.to_numeric(df['harvest_id'], errors='coerce').astype('Int64')

    df["year"] = (
        df["harvest_date"].dt.year
    )

    df["month"] = (
        df["harvest_date"].dt.month
    )

    df["day"] = (
        df["harvest_date"].dt.day
    )
    
    client_master = pd.read_csv("sample_data/client_master.csv")
    crop_master = pd.read_csv("sample_data/crop_master.csv")
    farm_master = pd.read_csv("sample_data/farm_master.csv")

    farm_master["farm_raw"] = farm_master["farm_raw"].map(norm_text)
    client_master["client_raw"] = client_master["client_raw"].map(norm_text)
    crop_master["crop_raw"] = crop_master["crop_raw"].map(norm_text)

    df = df.merge(
        farm_master,
        how="left",
        on="farm_raw",
    )
    
    df = df.merge(
        client_master,
        how="left",
        on="client_raw",
    )

    df = df.merge(
        crop_master,
        how="left",
        on="crop_raw",
    )

    return df
    
def main():
    harvest = load_raw_harvest()
    transformed = transform_harvest(harvest)

    print(transformed)

    print(
        transformed[
            [
                "harvest_id",
                "farm_raw",
                "farm_id",
                "client_raw",
                "client_id",
                "crop_raw",
                "crop_name",
            ]
        ]
    )

if __name__ == "__main__":
    main()
