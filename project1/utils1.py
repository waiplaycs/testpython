from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from pprint import pprint

# 提示模板
def generate_script(subject, video_length, creativity, api_key):
    # 定義生成標題的提示模板
    # ChatPromptTemplate.from_messages 用於創建一個基於聊天的提示模板
    # "human" 表示這是用戶的輸入，模板中使用 {subject} 作為佔位符
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")  # 為什麼用'' ? 因為需要將主題作為字符串嵌入
        ]
    )
    
    # 定義生成腳本的提示模板
    # 這裡的模板更複雜，包含了腳本的結構要求和維基百科搜索結果的參考
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human", """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
        ]
    )
    
    # 定義模型
    # ChatOpenAI 是一個基於 OpenAI 的聊天模型
    # model="deepseek-chat" 指定使用 DeepSeek 的聊天模型
    # openai_api_base 和 openai_api_key 用於設置 API 的基礎 URL 和密鑰
    # temperature 用於控制生成內容的創意程度，值越高越隨機
    model = ChatOpenAI(
        model="deepseek-chat",
        openai_api_base="https://api.deepseek.com",
        openai_api_key=api_key,
        temperature=creativity
    )
    
    # 將標題模板與模型鏈接，形成一個處理鏈
    # title_chain 是一個處理鏈，負責生成標題
    title_chain = title_template | model
    
    # 將腳本模板與模型鏈接，形成另一個處理鏈
    # script_chain 是一個處理鏈，負責生成腳本
    script_chain = script_template | model
    
    # 使用標題處理鏈生成標題
    # invoke 方法接受一個字典作為輸入，將 subject 傳遞給模板
    # 返回的內容是生成的標題
    title = title_chain.invoke({"subject": subject}).content
    
    # 使用 WikipediaAPIWrapper 進行維基百科搜索
    # lang="zh" 指定搜索語言為中文
    search = WikipediaAPIWrapper(lang="zh")
    # 根據主題進行搜索，返回搜索結果
    search_result = search.run(subject)
    
    # 使用腳本處理鏈生成腳本
    # 將生成的標題、視頻時長和維基百科搜索結果作為輸入
    # 返回的內容是生成的腳本
    script = script_chain.invoke({
        "title": title,
        "duration": video_length,
        "wikipedia_search": search_result
    }).content
    
    # 返回搜索結果、生成的標題和腳本
    return search_result, title, script

# 測試代碼（已註釋掉）
# result = generate_script("sora模型", 1, 0.7, "sk-a76cd8289e88452eba898431d3d0c3cf")
# pprint(result)
    