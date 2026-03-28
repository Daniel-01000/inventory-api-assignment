from pydantic import BaseModel, Field

class Product(BaseModel):
    ProductID: int = Field(..., description="Unique product ID")
    Name: str = Field(..., description="Product name")
    UnitPrice: float = Field(..., description="Price of the product")
    StockQuantity: int = Field(..., description="Number of items in stock")
    Description: str = Field(..., description="Product description")