import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional


class ChromaDBClient:
    def __init__(self, persist_directory: str = "data/chromadb"):
        self.client = chromadb.Client(
            Settings(persist_directory=persist_directory, anonymized_telemetry=False)
        )

    def create_collection(self, name: str, metadata: dict = None):
        return self.client.create_collection(name, metadata=metadata)

    def get_collection(self, name: str):
        return self.client.get_collection(name)

    def add_documents(
        self,
        collection_name: str,
        ids: list,
        documents: list,
        embeddings: list,
        metadata: list = None,
    ):
        collection = self.get_collection(collection_name)
        collection.add(
            ids=ids, documents=documents, embeddings=embeddings, metadatas=metadata
        )

    def query(self, collection_name: str, query_embedding: list, n_results: int = 5):
        collection = self.get_collection(collection_name)
        return collection.query(query_embeddings=[query_embedding], n_results=n_results)

    def delete_collection(self, name: str):
        return self.client.delete_collection(name)

    def list_collections(self):
        return self.client.list_collections()


if __name__ == "__main__":
    client = ChromaDBClient()
    coll = client.create_collection("test")
    print("ChromaDB connected successfully")
