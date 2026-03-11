from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Product API",
    description="API für Produktverwaltung (Starter-Version)",
    version="0.1.0"
)

# In-Memory Database (nur für Demo, geht beim Neustart verloren)
products_db = []


# ---------- Pydantic Models ----------

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    category: str
    stock: int = Field(..., ge=0)

    @validator("price")
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Preis muss positiv sein")
        return v


class ProductCreate(ProductBase):
    """Input-Modell für Produkt-Erstellung"""
    pass


class ProductUpdate(BaseModel):
    """Input-Modell für Produkt-Update (alle Felder optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """Output-Modell für API-Responses"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ---------- Helper ----------

def find_product(product_id: int):
    return next((p for p in products_db if p["id"] == product_id), None)


# ---------- Endpoints ----------

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/products/", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    """
    Erstellt ein neues Produkt.
    """
    product_dict = product.dict()
    now = datetime.now()

    product_dict["id"] = len(products_db) + 1
    product_dict["created_at"] = now
    product_dict["updated_at"] = now

    products_db.append(product_dict)
    return product_dict


@app.get("/products/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    """
    Gibt eine Liste von Produkten zurück.
    """

    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price darf nicht größer als max_price sein")

    result = products_db

    if category is not None:
        result = [p for p in result if p["category"] == category]

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    result = result[skip: skip + limit]

    return result


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """
    Gibt ein spezifisches Produkt zurück.
    """
    product = find_product(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")

    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_update: ProductUpdate):
    """
    Aktualisiert ein Produkt.
    """
    product = find_product(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")

    update_data = product_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        product[key] = value

    product["updated_at"] = datetime.now()

    return product


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int):
    """
    Löscht ein Produkt.
    """
    product = find_product(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")

    products_db.remove(product)
    return None
