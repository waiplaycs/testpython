import pandas as pd
import streamlit as st
from utils1 import dataframe_agent

def create_chart(input_data, chart_type):
    """
    根據輸入數據和圖表類型生成可視化。
    """
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)

# 設置頁面標題
st.title("csv數據分析工具💻✨🔍")

# 側邊欄輸入 OpenAI API key
with st.sidebar:
    openai_api_key = st.text_input("請輸入openai api key: ", type="password")
    st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

# 文件上傳控件
data = st.file_uploader("上傳你的數據文件 (csv格式) : ", type="csv")
if data:
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("raw data"):
        st.dataframe(st.session_state["df"])

# 用戶查詢輸入框，提供示例查詢
query = st.text_area(
    "请输入你关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图）：",
    placeholder="示例：\n1. 統計每個職業的數量並繪製條形圖\n2. 篩選年齡大於30的數據\n3. 繪製年齡與收入的散點圖"
)
button = st.button("生成回答")

# 檢查輸入條件
if button and not openai_api_key:
    st.info("請輸入你的openai api key")
elif button and "df" not in st.session_state:
    st.info("請先上傳數據文件")
elif button and openai_api_key and "df" in st.session_state:
    with st.spinner("ai is think..."):
        # 調用 dataframe_agent 函數
        response_dict = dataframe_agent(openai_api_key, st.session_state["df"], query)
        
        # 檢查是否返回錯誤
        if "error" in response_dict:
            st.error(response_dict["error"])
        else:
            # 顯示文本回答
            if "answer" in response_dict:
                st.write(response_dict["answer"])
            
            # 顯示表格
            if "table" in response_dict:
                st.table(pd.DataFrame(response_dict["table"]["data"], columns=response_dict["table"]["columns"]))
            
            # 顯示條形圖
            if "bar" in response_dict:
                create_chart(response_dict["bar"], "bar")
            
            # 顯示折線圖
            if "line" in response_dict:
                create_chart(response_dict["line"], "line")
            
            # 顯示散點圖
            if "scatter" in response_dict:
                create_chart(response_dict["scatter"], "scatter")
            
            
            
            
            
            
# sk-a76cd8289e88452eba898431d3d0c3cf