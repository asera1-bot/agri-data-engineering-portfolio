import pandas as pd
import os
from dotenv import load_dotenv

from src.extract.harvest import load_raw_harvest
from src.transform.harvest import transform_harvest
from src.validate.harvest import validate_harvest

from sqlalchemy import create_engine, text

def load_harvest(validated):
    fact_df = validated[
        validated["validation_status"].isin(
            ["OK", "WARNING"]
        )
    ].copy()

    quarantine_df = validated[
        validated["validation_status"] == "ERROR"
    ].copy()

    load_dotenv()

    DB_URL = (
        f"postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"localhost:{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

    engine = create_engine(DB_URL)

    with engine.begin() as conn:
        fact_df.to_sql(
            "fact_harvest",
            conn,
            if_exists="append",
            index=False,
        )

        quarantine_df.to_sql(
            "quarantine_harvest",
            conn,
            if_exists="append",
            index=False,
        )

def main():
    harvest = load_raw_harvest()
    transformed = transform_harvest(harvest)
    validated = validate_harvest(transformed)

    load_harvest(validated)

if __name__ == "__main__":
    main()
