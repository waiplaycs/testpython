from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 定義問答代理函數
def qa_agent(openai_api_key, memory, uploaded_file, question):
    # 1. 配置聊天模型
    # 使用 DeepSeek 聊天模型，設置 API 基礎 URL 和密鑰
    model = ChatOpenAI(
        model="deepseek-chat",  # 指定使用的模型
        openai_api_base="https://api.deepseek.com",  # API 基礎 URL
        openai_api_key=openai_api_key  # 用戶提供的 API 密鑰
    )
    
    # 2. 處理上傳的 PDF 文件
    # 讀取文件內容並保存到臨時文件
    file_content = uploaded_file.read()
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)
        
    # 使用 PyPDFLoader 加載 PDF 文件
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()  # 將 PDF 文件轉換為文檔對象
    
    # 3. 分割文本
    # 使用 RecursiveCharacterTextSplitter 將文檔分割為小塊
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # 每塊的最大字符數
        chunk_overlap=50,  # 每塊之間的重疊字符數
        separators=["\n", "。", "！", "？", "，", "、", " ", ""]  # 分割符
    )
    texts = text_splitter.split_documents(docs)  # 分割文檔
    
    # 4. 使用本地嵌入模型
    # 使用 HuggingFace 的嵌入模型生成向量
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(texts, embeddings_model)  # 創建向量存儲
    retriever = db.as_retriever()  # 構建檢索器
    
    # 5. 構建問答鏈
    # 使用 ConversationalRetrievalChain 將聊天模型與檢索器結合
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,  # 聊天模型
        retriever=retriever,  # 文檔檢索器
        memory=memory  # 對話記憶
    )
    
    # 6. 執行問答
    # 傳入對話歷史和用戶問題，執行問答
    response = qa.invoke({"chat_history": memory, "question": question})
    
    # 7. 返回結果
    # 返回包含回答和對話歷史的結果
    return response





