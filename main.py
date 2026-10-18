from fastapi import FastAPI
from sqlmodel import SQLModel
import database as db
import models
from rag.build_db import build_database
from routers import products, reviews, chat

app = FastAPI()

app.include_router(products.router)
app.include_router(reviews.router)
app.include_router(chat.router)
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(db.engine)
    build_database()

@app.get("/")
def read_root():
    return {"messages": "欢迎来到电商导购系统"}