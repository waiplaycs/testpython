import streamlit as st
from utils1 import qa_agent
from langchain.memory import ConversationBufferMemory
import os

# 設置應用的標題
st.title("ai智能pdf問答工具")

# 側邊欄輸入區域
with st.sidebar:
    # 用戶輸入 OpenAI API 密鑰，密碼類型輸入框
    openai_api_key = st.text_input("請輸入openai api key: ", type="password")
    # 提供獲取 OpenAI API 密鑰的鏈接
    st.markdown("[獲取openai api key](https://api-docs.deepseek.com/)")

# 初始化對話記憶
if "memory" not in st.session_state:
    # ConversationBufferMemory 用於存儲對話歷史，支持多輪對話
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,  # 返回消息格式
        memory_key="chat_history",  # 記憶的鍵
        output_key="answer"  # 模型輸出的鍵
    )

# 文件上傳區域
uploaded_file = st.file_uploader("上傳你的pdf文件: ", type="pdf")  # 限制文件類型為 PDF

# 問題輸入框，只有在文件上傳後才可用
question = st.text_input("對pdf的內容進行提問", disabled=not uploaded_file)

# 如果用戶提供了文件、問題和 API 密鑰，則執行問答
if uploaded_file and question and openai_api_key:
    # 顯示加載提示，表示 AI 正在處理
    with st.spinner("ai正在思考中, 請稍等..."):
        # 調用後端函數執行問答
        response = qa_agent(openai_api_key, st.session_state["memory"], uploaded_file, question)
    
    # 顯示 AI 的回答
    st.write("### answer")
    st.write(response["answer"])
    
    # 更新對話歷史
    st.session_state["chat_history"] = response["chat_history"]

# 如果有對話歷史，顯示歷史消息
if "chat_history" in st.session_state:
    with st.expander("history messages"):
        # 遍歷對話歷史，按人類和 AI 消息交替顯示
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.write(human_message.content)  # 顯示人類消息
            if i < len(st.session_state["chat_history"]) - 2:
                st.divider()  # 添加分隔線
    
# sk-a76cd8289e88452eba898431d3d0c3cf