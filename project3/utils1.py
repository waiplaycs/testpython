from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import os

# 定義函數以獲取聊天回應
def get_chat_response(prompt, memory, openai_api_key):
    # 1. 初始化聊天模型
    # 使用 ChatOpenAI 定義聊天模型，設置模型名稱和 API 基礎 URL 以及密鑰
    model = ChatOpenAI(
        model="deepseek-chat",  # 指定使用的模型
        openai_api_base="https://api.deepseek.com",  # API 基礎 URL
        openai_api_key=openai_api_key  # 用戶提供的 API 密鑰
    )
    
    # 2. 創建對話鏈
    # ConversationChain 將聊天模型與記憶結合，實現多輪對話
    chain = ConversationChain(llm=model, memory=memory)
    
    # 3. 執行對話鏈
    # 調用 chain.invoke() 方法，傳入用戶的輸入提示
    response = chain.invoke({"input": prompt})
    
    # 4. 返回回應
    # 提取並返回模型生成的回應
    return response["response"]

# 初始化對話記憶
# ConversationBufferMemory 用於存儲對話歷史，支持多輪對話
memory = ConversationBufferMemory(return_messages=True)

# 測試代碼（已註釋掉）
# print(get_chat_response("牛頓提出過哪些知名的定律?", memory, os.getenv("OPENAI_API_KEY")))
# print(get_chat_response("我上一個問題是什麼??", memory, os.getenv("OPENAI_API_KEY")))
    
    
    
    
    
    