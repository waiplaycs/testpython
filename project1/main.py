import streamlit as st 
from utils1 import generate_script

# 設置應用的標題
st.title("影片腳本生成器")

# 在側邊欄中添加輸入框和說明
with st.sidebar:
    # 用戶輸入 DeepSeek API 密鑰，密碼類型輸入框
    deepseek_api_key = st.text_input("請輸入deepseek api key ", type="password")
    # 提供獲取 DeepSeek API 密鑰的鏈接
    st.markdown("[獲取deepseek api key](https://api-docs.deepseek.com)")

# 用戶輸入影片主題
subject = st.text_input("請輸入影片主題")
# 用戶輸入影片的預計時長，最小值為 0.1 分鐘，步長為 0.1
video_length = st.number_input("請輸入大致時長 (單位: 分鐘) ", min_value=0.1, step=0.1) 
# 用戶選擇創意程度的滑塊，範圍為 0.0 到 1.0，默認值為 0.2
creativity = st.slider("creativity: ", min_value=0.0, max_value=1.0, value=0.2, step=0.1)

# 按鈕觸發腳本生成
submit = st.button("生成腳本")

# 驗證用戶是否輸入了 API 密鑰，若未輸入則提示並停止執行
if submit and not deepseek_api_key:
    st.info("please type in your openai api key")
    st.stop()

# 驗證用戶是否輸入了影片主題，若未輸入則提示並停止執行
if submit and not subject:
    st.info("please type in your theme of video")
    st.stop()   

# 驗證用戶輸入的影片時長是否大於等於 0.1，若不符合則提示並停止執行
if submit and not video_length >= 0.1:          
    st.info("vid length must be >= 0.1")
    st.stop()   

# 如果所有條件都滿足，開始生成腳本
if submit:
    # 顯示加載提示，表示正在生成腳本
    with st.spinner(("ai generating, please wait...")):
        # 調用 generate_script 函數生成腳本，返回搜索結果、標題和腳本內容
        search_result, title, script = generate_script(subject, video_length, creativity, deepseek_api_key)
    
    # 顯示成功提示
    st.success("script generation complete! ")
    # 顯示生成的影片標題
    st.subheader("🤡🔥 title: ")
    st.write(title)
    # 顯示生成的影片腳本
    st.subheader("📋 script: ")
    st.write(script)
    # 展開區域顯示相關的維基搜索結果
    with st.expander("wiki search result: 😎"):
        st.info(search_result)


