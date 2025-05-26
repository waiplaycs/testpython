# frontend
import streamlit as st
from utils1 import generate_xiaohongshu

# 設置應用的標題
st.header("爆款小紅書寫作助手")

# 側邊欄輸入區域
with st.sidebar:
    # 用戶輸入 OpenAI API 密鑰，密碼類型輸入框
    openai_api_key = st.text_input("請輸入openai api key: ", type="password")
    # 提供獲取 OpenAI API 密鑰的鏈接
    st.markdown("[獲取openai api key] (https://platform.deepseek.com/api_keys)")

# 用戶輸入主題
theme = st.text_input("主題")

# 按鈕觸發寫作
submit = st.button("開始寫作")

# 驗證用戶是否輸入了 API 密鑰，若未輸入則提示並停止執行
if submit and not openai_api_key:
    st.info("請輸入你的openai api key")
    st.stop()

# 驗證用戶是否輸入了主題，若未輸入則提示並停止執行
if submit and not theme:
    st.info("請輸入生成內容的主題")
    st.stop()

# 如果用戶點擊按鈕且輸入有效，開始生成內容
if submit:
    # 顯示加載提示，表示正在生成內容
    with st.spinner("ai正在努力創作中,請稍等..."):
        # 調用後端函數生成小紅書內容
        result = generate_xiaohongshu(theme, openai_api_key)
    
    # 添加分隔線
    st.divider()
    
    # 創建兩列佈局
    left_column, right_column = st.columns(2)
    
    # 左側顯示生成的標題
    with left_column:
        st.markdown("##### 小紅書標題1")
        st.write(result.titles[0])
        st.markdown("##### 小紅書標題2")
        st.write(result.titles[1])
        st.markdown("##### 小紅書標題3")
        st.write(result.titles[2])
        st.markdown("##### 小紅書標題4")
        st.write(result.titles[3])
        st.markdown("##### 小紅書標題5")
        st.write(result.titles[4])
    
    # 右側顯示生成的正文
    with right_column:
        st.markdown("##### 小紅書正文")
        st.write(result.content)











