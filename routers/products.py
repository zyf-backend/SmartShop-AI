from fastapi import APIRouter
from fastapi import HTTPException
from models import Product
from sqlmodel import select
from database import SessionDep

router = APIRouter()


@router.get("/products")
async def get_products(
    session: SessionDep,
    category: str | None = None,
    limit: int = 10
):
    statement = select(Product)
    if category:
        statement = statement.where(Product.category == category)
    products = session.exec(statement.limit(limit)).all()
    return products

@router.get("/products/{product_id}")
async def get_product(
        session:SessionDep,
        product_id: int,
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products")
async def add_product(
        product: Product,
        session: SessionDep
):
    existing = session.exec(select(Product).where(Product.name == product.name)).first()
    if  existing:
        raise HTTPException(status_code=400, detail="Product already exists")
    session.add(product)
    session.commit()
    session.refresh(product)
    return {"messages":"Product added"}

@router.delete("/products/{product_id}")
async def delete_product(
        session: SessionDep,
        product_id: int
):
    existing = session.exec(select(Product).where(Product.id == product_id)).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(existing)
    session.commit()
    return {"messages":"Product deleted"}
