import os
import json

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document


class ChromaDB:
    __instance = None

    @staticmethod
    def getInstance():
        if ChromaDB.__instance is None:
            ChromaDB()
        return ChromaDB.__instance

    def __init__(self):
        if ChromaDB.__instance is not None:
            raise Exception("ChromaDB is a singleton!")
        else:
            cwd = os.getcwd()
            ABS_PATH: str = cwd
            persist_directory = 'db'
            DB_DIR: str = os.path.join(ABS_PATH, persist_directory)
            embedding_model="nomic-embed-text"
            embeddings = OllamaEmbeddings(model=embedding_model)
            ChromaDB.__instance = Chroma(
                    embedding_function=embeddings,
                    persist_directory=DB_DIR,
                    collection_name=embedding_model
            )
            

def get_ChromaDB_Retriever():
    vectorDB = ChromaDB.getInstance()
    return vectorDB.as_retriever()

def search_with_score(question):
    vectorDB = ChromaDB.getInstance()
    results = vectorDB.similarity_search_with_score(question)
    return results

searchResults = search_with_score("修定的方法為何？")

for doc in searchResults:
    file_name = os.path.basename(doc[0].metadata['source'])
    print(str(doc[1]) + " " + str(doc[0].metadata['page']) + " " + file_name )
    print(doc[0].page_content)    