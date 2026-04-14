from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
from typing import List, Dict, Optional


class QdrantClientWrapper:
    def __init__(self, url: str = None, api_key: str = None):
        self.client = QdrantClient(
            url=url or os.getenv("QDRANT_URL", "localhost"),
            api_key=api_key or os.getenv("QDRANT_API_KEY"),
        )

    def create_collection(self, name: str, vector_size: int = 1536):
        self.client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def upsert(self, collection_name: str, points: List[PointStruct]):
        self.client.upsert(collection_name=collection_name, points=points)

    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 5,
        filter: dict = None,
    ):
        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=filter,
        )

    def delete_collection(self, name: str):
        self.client.delete_collection(name)

    def get_collections(self):
        return self.client.get_collections()


if __name__ == "__main__":
    client = QdrantClientWrapper()
    print("Qdrant client initialized")
