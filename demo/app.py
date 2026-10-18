import streamlit as st
import requests

st.title("🛍️ AI 电商导购助手")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史聊天
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 接收用户输入
if prompt := st.chat_input("想买点什么？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 调用你的 FastAPI 接口
    with st.spinner("思考中..."):
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"question": prompt}
        )
        answer = response.json().get("answer", "出错了")

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)