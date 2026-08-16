import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"localhost:{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DB_URL)

st.title("Agricultural Data Engineering Portfolio")

fact = pd.read_sql(
    "SELECT * FROM fact_harvest",
    engine,
)

st.metric(
    "Total Yield (g)",
    f"{fact['quantity_g'].sum():,.0f}",
)

farm_yield = (
    fact.groupby("farm_id", as_index=False)["quantity_g"]
    .sum()
)

st.subheader("Yield by Farm")
st.bar_chart(
    farm_yield.set_index("farm_id")
)

crop_yield = (
    fact.groupby("crop_name", as_index=False)["quantity_g"]
    .sum()
)

st.subheader("Yield by Crop")
st.bar_chart(
    crop_yield.set_index("crop_name")
)

st.subheader("Data Quality")

quality = (
    fact["validation_status"]
    .value_counts()
)

st.bar_chart(quality)

st.subheader("Warning Records")

st.dataframe(
    fact[
        fact["validation_status"] == "WARNING"
    ]
)
