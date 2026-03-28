import pandas as pd
from database import products_collection

# Read the CSV file
df = pd.read_csv("products.csv")

# Convert CSV rows into a list of dictionaries
products = df.to_dict(orient="records")

# Clear old data first so you do not get duplicates
products_collection.delete_many({})

# Insert new data
result = products_collection.insert_many(products)

print(f"Inserted {len(result.inserted_ids)} products into MongoDB.")