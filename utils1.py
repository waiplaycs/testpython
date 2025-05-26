# 導入所需的 Python 模組
import json  # 用於處理和解析 JSON 數據
import pandas as pd  # 用於操作和轉換 DataFrame 數據
import requests  # 用於發送 HTTP 請求到外部 API
import re  # 用於正則表達式，以靈活處理 Markdown 標記（如去除 ```json 和 ```）

# 定義函數，處理用戶查詢並返回數據分析結果
def dataframe_agent(api_key, df, query):
    """
    處理用戶查詢並返回分析結果（文本、表格或圖表數據）。

    參數：
        api_key (str): DeepSeek API key，用於認證 API 請求
        df (pd.DataFrame): 輸入的數據表格，包含需要分析的數據
        query (str): 用戶的查詢或可視化要求，例如統計、篩選或圖表生成

    返回：
        dict: 包含分析結果的字典，可能包括文本回答、表格或圖表數據
    """
    # 定義 DeepSeek API 的端點 URL
    api_url = "https://api.deepseek.com/v1/chat/completions"

    # 構建 HTTP 請求的標頭，包含認證信息和內容類型
    headers = {
        "Authorization": f"Bearer {api_key}",  # 使用 Bearer token 進行身份驗證
        "Content-Type": "application/json"     # 指定請求體為 JSON 格式
    }

    # 使用 try-except 塊捕獲潛在錯誤，確保程式穩定性
    try:
        # 將 Pandas DataFrame 轉換為 CSV 格式的字符串，以便傳遞給 API
        df_str = df.to_csv(index=False)  # index=False 表示不包含行索引，避免冗餘數據

        # 構建提示詞（prompt），將數據和用戶查詢傳遞給 API
        prompt = f"""
        你是一個數據分析助手。以下是 CSV 數據：
        {df_str}

        用戶查詢：{query}

        請分析數據並返回結果，格式為 JSON，包含以下字段（根據需要）：
        - "answer": 文本回答（如果適用）
        - "table": 表格數據，包含 "data"（列表）和 "columns"（列名列表）
        - "bar": 條形圖數據，包含 "data" 和 "columns"
        - "line": 折線圖數據，包含 "data" 和 "columns"
        - "scatter": 散點圖數據，包含 "data" 和 "columns"

        如果查詢不夠具體，請返回：
        {{"answer": "請提供具體的數據分析問題或請求，例如統計、篩選、可視化等。"}}

        確保響應是有效的 JSON 格式。
        """

        # 構建 API 請求的數據體，符合 DeepSeek API 的格式要求
        data = {
            "model": "deepseek-chat",  # 指定使用的模型名稱（需確認是否為 DeepSeek 的正確模型）
            "messages": [              # 對話結構，包含系統指令和用戶提示
                {"role": "system", "content": "你是一個數據分析助手，返回 JSON 格式的結果。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000  # 設置生成的最大 token 數量，可根據需求調整
        }

        # 發送 POST 請求到 DeepSeek API，傳遞 headers 和 data
        response = requests.post(api_url, headers=headers, json=data)

        # 檢查 HTTP 響應狀態碼，確保請求成功
        if response.status_code != 200:
            # 如果狀態碼不是 200，表示請求失敗，拋出異常並提供錯誤詳情
            raise Exception(f"API 請求失敗，狀態碼：{response.status_code}, 訊息：{response.text}")

        # 解析 API 返回的 JSON 格式響應
        response_json = response.json()

        # 提取模型生成的文本內容（假設響應結構與 OpenAI API 類似）
        output = response_json["choices"][0]["message"]["content"]

        # 打印原始 API 輸出，方便調試和檢查
        print("API 原始輸出：", output)

        # 使用正則表達式去除 Markdown 代碼塊標記（```json 和 ```），確保得到純 JSON 字符串
        # re.sub 替換匹配的模式，flags=re.MULTILINE 支持多行文本處理
        output = re.sub(r'^```json\s*|\s*```$', '', output, flags=re.MULTILINE).strip()

        # 嘗試將處理後的輸出解析為 Python 字典
        try:
            response_dict = json.loads(output)  # 將 JSON 字符串轉換為字典
            return response_dict  # 返回解析後的結果字典
        except json.JSONDecodeError as e:
            # 如果 JSON 解析失敗，打印錯誤信息並返回錯誤字典
            print(f"JSON 解析錯誤：{e}")
            print(f"無效的輸出內容：{output}")
            return {"error": f"無法解析 API 響應為 JSON：{str(e)}"}

    except Exception as e:
        # 捕獲其他異常（如網絡問題、無效 API key 等），並返回錯誤信息
        print(f"API 調用錯誤：{e}")
        return {"error": f"API 調用失敗：{str(e)}"}