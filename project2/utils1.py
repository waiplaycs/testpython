# backend

from prompt_template import system_template_text, user_template_text
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from xiaohongshu_model import Xiaohongshu
from pprint import pprint

# 定義生成小紅書內容的函數
def generate_xiaohongshu(theme, openai_api_key):
    # 1. 創建提示模板
    # 使用 ChatPromptTemplate 定義系統和用戶的提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_text),  # 系統提示，包含寫作規則和格式
        ("user", user_template_text)       # 用戶提示，包含主題
    ])
    
    # 2. 定義模型
    # 使用 ChatOpenAI 定義聊天模型，設置 API 基礎 URL 和密鑰
    model = ChatOpenAI(
        model="deepseek-chat",                   # 指定使用的模型
        openai_api_base="https://api.deepseek.com",  # API 基礎 URL
        openai_api_key=openai_api_key           # 用戶提供的 API 密鑰
    )
    
    # 3. 定義輸出解析器
    # 使用 PydanticOutputParser 將模型輸出的數據解析為 Xiaohongshu 類型
    output_parser = PydanticOutputParser(pydantic_object=Xiaohongshu)
    
    # 4. 串聯處理鏈
    # 將提示模板、模型和解析器串聯起來，形成完整的處理鏈
    chain = prompt | model | output_parser
    
    # 5. 執行處理鏈
    # 調用 chain.invoke() 方法，傳入主題和解析器的格式說明
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),  # 解析器的格式說明
        "theme": theme  # 用戶輸入的主題
    })
    
    # 6. 返回結果
    # 返回解析後的結果，包含標題和正文
    return result

# 測試代碼（已註釋掉）
# result = generate_xiaohongshu("大模型", "sk-a76cd8289e88452eba898431d3d0c3cf")
# pprint(result)

