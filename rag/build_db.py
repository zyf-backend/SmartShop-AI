from rag.loader import db
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def build_database():
    """自动检查并建库的函数"""
    if db._collection.count() > 0:
        print(f"向量库已有 {db._collection.count()} 条数据，跳过加载。")
        return

    urls = [
        "https://www.gov.cn/zhengce/zhengceku/2020-11/03/content_5557118.htm",
        "https://school.jinritemai.com/doudian/web/articlev0/101835",
        "https://scjgj.quanzhou.gov.cn/xxgk/ztzl/xfts/xfjs/202501/t20250127_3136187.htm"
    ]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 500,
        chunk_overlap= 50,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", ".", "!", "?", ";", ",", " ", ""]
    )

    print("1. 开始载入网页...")
    loader = WebBaseLoader(urls)
    docs = loader.load()

    print("2. 开始切分...")
    chunks = text_splitter.split_documents(docs)

    print("3. 存入向量库...")
    db.add_documents(chunks)
    print(f"完成！成功存入 {len(chunks)} 个碎片。")