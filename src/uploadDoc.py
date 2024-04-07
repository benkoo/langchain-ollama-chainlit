import PyPDF2
import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader

persist_directory = 'db'

cwd = os.getcwd()

ABS_PATH: str = cwd
DB_DIR: str = os.path.join(ABS_PATH, persist_directory)
DATA_DIR: str = os.path.join(ABS_PATH, "data")

print(ABS_PATH)
print(DB_DIR)
print(DATA_DIR)

loader = DirectoryLoader(DATA_DIR, glob="./*.pdf", loader_cls=PyPDFLoader)

documents = loader.load()

print(len(documents))


print(documents[6])

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

print(len(texts))

print(texts[6])


embedding_model="nomic-embed-text"

embeddings = OllamaEmbeddings(model=embedding_model)


vectordb = Chroma.from_documents(documents=texts, 
                                 embedding=embeddings,
                                 persist_directory=persist_directory,
                                 collection_name=embedding_model
                                 )

vectordb.persist()

retriever=vectordb.as_retriever()

question="故事"
results = retriever.invoke(question)
print(results)