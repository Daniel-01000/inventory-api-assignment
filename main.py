from fastapi import FastAPI, HTTPException, Query
from models import Product
from database import products_collection
import requests

app = FastAPI(title="Inventory Management API")


@app.get("/")
def home():
    return {"message": "Inventory API is running"}


@app.get("/getAll")
def get_all():
    products = list(products_collection.find({}, {"_id": 0}))
    return products


@app.get("/getSingleProduct")
def get_single_product(product_id: int = Query(..., description="Product ID")):
    product = products_collection.find_one({"ProductID": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/addNew")
def add_new(product: Product):
    products_collection.delete_one({"ProductID": product.ProductID})
    products_collection.insert_one(product.model_dump())
    return {"message": "Product added successfully"}


@app.delete("/deleteOne")
def delete_one(product_id: int = Query(..., description="Product ID")):
    result = products_collection.delete_one({"ProductID": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


@app.get("/startsWith")
def starts_with(letter: str = Query(..., min_length=1, max_length=1, description="Starting letter")):
    products = list(
        products_collection.find(
            {"Name": {"$regex": f"^{letter}", "$options": "i"}},
            {"_id": 0}
        )
    )
    return products


@app.get("/paginate")
def paginate(start_id: int = Query(...), end_id: int = Query(...)):
    products = list(
        products_collection.find(
            {"ProductID": {"$gte": start_id, "$lte": end_id}},
            {"_id": 0}
        ).sort("ProductID", 1).limit(10)
    )
    return products


@app.get("/convert")
def convert(product_id: int = Query(..., description="Product ID")):
    product = products_collection.find_one({"ProductID": product_id}, {"_id": 0})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    usd_price = product["UnitPrice"]

    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Could not fetch exchange rate")

    data = response.json()
    eur_rate = data["rates"]["EUR"]
    eur_price = round(usd_price * eur_rate, 2)

    return {
        "ProductID": product["ProductID"],
        "Name": product["Name"],
        "PriceUSD": usd_price,
        "PriceEUR": eur_price
    }