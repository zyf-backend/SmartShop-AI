
from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
     id: int | None = Field(default=None, primary_key=True )
     name: str = Field(index=True)
     category: str
     price: float
     stock: int
     description: str
     rating: float = 0.0

class Review(SQLModel, table=True):
     id: int | None = Field(default=None, primary_key=True )
     product_id: int = Field(index=True)  # 关联 Product 的 id
     user_name: str
     rating: float
     content: str
