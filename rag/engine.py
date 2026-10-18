import os

from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

from rag.build_db import build_database
from rag.loader import db
from rag.tools import search_products, check_product_stock, get_product_reviews, search_store_policy

load_dotenv(override=True)
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

deepseek = ChatOpenAI(
    api_key= os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    model="deepseek-flash"
)

prompt="""你是一名专业的电商金牌管家。
你可以调用工具来回答用户的问题：
1. 如果用户问商品推荐、价格、库存，请调用商品相关的工具。
2. 如果用户问退换货政策、保修规则，【必须】调用 search_store_policy 工具检索知识库，严禁自己瞎编规则。
请根据查到的信息热情、专业地回答。"""


agent =create_agent(
    model=deepseek,
    tools=[search_products,check_product_stock,get_product_reviews,search_store_policy],
    system_prompt=prompt
)


def run_agent(question: str):
    response = agent.invoke({
        "messages":[{
            "role":    "user",
            "content":question
        }]
    })
    return {"answer":response["messages"][-1].content}


