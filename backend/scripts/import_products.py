import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# Read H&M articles dataset
df = pd.read_csv("../../ml/data/raw/articles.csv")

# Keep useful columns only
df = df[
    [
        "article_id",
        "prod_name",
        "product_type_name",
        "product_group_name",
        "colour_group_name",
        "detail_desc"
    ]
]

# Rename columns to match DB
df.rename(columns={
    "prod_name": "product_name",
    "detail_desc": "description"
}, inplace=True)

# Optional: Add dummy price
df["price"] = 999

# Optional image URL
df["image_url"] = None
df["product_url"] = None

# Insert into PostgreSQL
df.to_sql(
    "products",
    engine,
    if_exists="append",
    index=False
)

print("Products imported successfully!")