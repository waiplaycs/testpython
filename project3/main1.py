import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils1 import get_chat_response

# 設置應用的標題
st.title("clone chatgpt 666 😊😎💻")

# 側邊欄輸入區域
with st.sidebar:
    # 用戶輸入 OpenAI API 密鑰，密碼類型輸入框
    openai_api_key = st.text_input("請輸入openai api key: ", type="password")
    # 提供獲取 OpenAI API 密鑰的鏈接
    st.markdown("[獲取openai api key](https://api-docs.deepseek.com/)")
    
    # 清除對話歷史的按鈕
    if st.button("clear history"):
        # 重置對話記憶和消息列表
        st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
        st.session_state["messages"] = [{"role": "ai", "content": "你好,我是你的ai助手,有什麼可以幫你的嗎😊?"}]

# 初始化對話記憶和消息列表
if "memory" not in st.session_state:
    # 初始化對話記憶
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    # 初始化消息列表，包含 AI 的歡迎消息
    st.session_state["messages"] = [{"role": "ai", "content": "你好,我是你的ai助手,有什麼可以幫你的嗎😊?"}]

# 顯示對話歷史
for message in st.session_state["messages"]:
    # 根據消息角色（human 或 ai）顯示對話內容
    st.chat_message(message["role"]).write(message["content"])

# 用戶輸入框
prompt = st.chat_input()
if prompt:
    # 如果用戶未輸入 API 密鑰，提示並停止執行
    if not openai_api_key:
        st.info("請輸入你的openai api key")
        st.stop()
    
    # 將用戶輸入的消息添加到消息列表
    st.session_state["messages"].append({"role": "human", "content": prompt})
    # 顯示用戶的輸入消息
    st.chat_message("human").write(prompt)
    
    # 顯示加載提示，表示 AI 正在生成回應
    with st.spinner("ai正在思考中,請稍等..."):
        # 調用後端函數獲取 AI 回應
        response = get_chat_response(prompt, st.session_state["memory"], openai_api_key)
    
    # 將 AI 的回應添加到消息列表
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    # 顯示 AI 的回應消息
    st.chat_message("ai").write(response)

# 測試代碼（已註釋掉）
# sk-a76cd8289e88452eba898431d3d0c3cf
# 全球最高的大樓是哪裡?