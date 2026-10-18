import os
from dotenv import load_dotenv
from langchain_chroma import Chroma

from langchain_community.embeddings import DashScopeEmbeddings

load_dotenv(override=True)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v1",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

db =Chroma(
    collection_name="shopping_rules",
    embedding_function=embeddings,
    persist_directory="./shopping_chroma_db"
)

