import pinecone
import os
from typing import List, Dict, Optional


class PineconeClient:
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        environment = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
        if api_key:
            pinecone.init(api_key=api_key, environment=environment)
        self._indexes = {}

    def create_index(self, name: str, dimension: int = 1536, metric: str = "cosine"):
        if name not in pinecone.list_indexes():
            pinecone.create_index(name=name, dimension=dimension, metric=metric)
        self._indexes[name] = pinecone.Index(name)
        return self._indexes[name]

    def get_index(self, name: str):
        if name not in self._indexes:
            self._indexes[name] = pinecone.Index(name)
        return self._indexes[name]

    def upsert_vectors(self, index_name: str, vectors: list):
        index = self.get_index(index_name)
        index.upsert(vectors=vectors)

    def query(
        self, index_name: str, query_vector: list, top_k: int = 5, filter: dict = None
    ):
        index = self.get_index(index_name)
        return index.query(vector=query_vector, top_k=top_k, filter=filter or {})

    def delete_index(self, name: str):
        pinecone.delete_index(name)
        if name in self._indexes:
            del self._indexes[name]

    def list_indexes(self):
        return pinecone.list_indexes()


if __name__ == "__main__":
    client = PineconeClient()
    print("Pinecone client initialized")
