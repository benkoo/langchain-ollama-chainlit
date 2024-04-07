import os
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from langchain_community.embeddings import OllamaEmbeddings


cwd = os.getcwd()

ABS_PATH: str = cwd


persist_directory = 'db'

DB_DIR: str = os.path.join(ABS_PATH, persist_directory)

client = PersistentClient(path=DB_DIR)


embedding_model="nomic-embed-text"

default_ef = embedding_functions.(model_name=embedding_model)

myCollection = client.get_collection(name=embedding_model)

val = default_ef(["廣欽⽼和尚"])

results = myCollection.query(
    query_embeddings=val,
    n_results=10,
    where={"metadata_field": "is_equal_to_this"},
    where_document={"$contains":"search_string"}
)


print(results)