from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 현재 실행 중인 파일의 디렉터리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# 상대 경로 설정
file_name = os.path.join(current_dir, "소나기.pdf")

print(f"파일 경로: {file_name}")  # 디버깅용

loader = PyPDFLoader(file_name)
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

#embeddings = HuggingFaceEmbeddings()
embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)

from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import FAISS

index = VectorstoreIndexCreator(
    vectorstore_cls=FAISS,
    embedding=embeddings,
    ).from_loaders([loader])

# 파일로 저장
index.vectorstore.save_local("shower")
