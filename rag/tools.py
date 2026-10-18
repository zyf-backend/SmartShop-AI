from langchain_core.tools import tool
from pydantic import BaseModel, Field
from sqlmodel import Session, select

# 导入你的数据库配置和模型
from database import engine
from models import Product, Review
from rag.loader import db


# 1. 定义参数结构（可选，但推荐，能让模型更清晰）
class SearchInput(BaseModel):
    keyword: str = Field(description="搜索关键词，比如 '手机'、'联想'、'耳机'")

class StockInput(BaseModel):
    product_name: str = Field(description="商品名称")

class ReviewInput(BaseModel):
    product_name: str = Field(description="商品名称")


# 2. 用 @tool 装饰器定义工具
@tool(args_schema=SearchInput)
def search_products(keyword: str) -> str:
    """根据关键词在商城中搜索商品。当用户想要购买某类商品或查找特定品牌时使用此工具。"""
    with Session(engine) as session:
        # 模糊查询商品名或分类
        statement = select(Product).where(
            (Product.name.contains(keyword)) | (Product.category.contains(keyword))
        )
        results = session.exec(statement).all()

        if not results:
            return f"没有找到与 '{keyword}' 相关的商品。"

        # 把查到的商品拼成字符串返回给大模型
        info = []
        for p in results:
            info.append(f"商品名：{p.name}，分类：{p.category}，价格：{p.price}元，库存：{p.stock}件")

        return "\n".join(info)

@tool(args_schema=StockInput)
def check_product_stock(product_name: str) -> str:
    """根据商品名称查询商品库存。当用户询问某商品库存余量时使用此工具。"""
    with Session(engine) as session:
        statement = select(Product).where(Product.name.contains(product_name))
        results = session.exec(statement).first()
        if not results:
            return f"没有找到名为'{product_name}'的商品 "
        return f"{results.name}当前库存剩余: {results.stock}件,价格为 {results.price}元。"

@tool(args_schema=ReviewInput)
def get_product_reviews(product_name: str) -> str:
    """根据商品名称查询对应的商品评论。当用户想要得知某商品的口碑或你要综合是商品口碑给出购买建议时使用此工具。"""
    with Session(engine) as session:
        statement = select(Product).where(Product.name.contains(product_name))
        results = session.exec(statement).first()
        if not results:
            return f"没有找到名为'{product_name}'的商品 "
        info = [f"商品{results.name}的评价如下："]
        statement = select(Review).where(Review.product_id == results.id)
        reviews = session.exec(statement).all()
        if not reviews:
            return f"商品{results.name}暂无评价"
        for r in reviews:
            info.append(f"用户 {r.user_name} (打分 {r.rating}): {r.content}")
        return "\n".join(info)

@tool
def search_store_policy(content: str) -> str:
    """从数据库中查询问题答复,当需要解答购物相关问题时使用此工具

    Args:
        content: 想要查询的内容/关键词/问题
    """
    docs = db.similarity_search(content,k=3)
    if not docs:
        return "未查询到相关信息"
    return "\n".join(doc.page_content for doc in docs)