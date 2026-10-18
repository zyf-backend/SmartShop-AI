from fastapi import APIRouter
from fastapi import HTTPException
from models import Review,Product
from sqlmodel import select
from database import SessionDep

router = APIRouter()


@router.get("/reviews/{product_id}")
async def get_reviews(
        session: SessionDep,
        product_id: int,
):
    product = session.get(Product,product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    statement = session.exec(select(Review).where(Review.product_id == product_id)).all()


    return statement

@router.post("/reviews")
async def create_review(
        session: SessionDep,
        review: Review,
):
    product = session.get(Product,review.product_id )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.add(review)
    session.commit()
    session.refresh(review)
    return {"message":"Review added"}

@router.delete("/reviews/{review_id}")
async def delete_product(
        session: SessionDep,
        review_id: int
):
    existing = session.exec(select(Review).where(Review.id == review_id)).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(existing)
    session.commit()
    return {"message":"Review deleted"}
