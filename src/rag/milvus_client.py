from pymilvus import (
    connections,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
    utility,
)
from typing import List, Dict, Optional


class MilvusClient:
    def __init__(self, host: str = "localhost", port: str = "19530"):
        connections.connect(host=host, port=port)
        self._collections = {}

    def create_collection(self, name: str, dimension: int = 1536):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
        ]
        schema = CollectionSchema(fields, description=f"{name} collection")
        collection = Collection(name, schema)

        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128},
        }
        collection.create_index("vector", index_params)

        self._collections[name] = collection
        return collection

    def get_collection(self, name: str):
        if name not in self._collections:
            self._collections[name] = Collection(name)
        return self._collections[name]

    def insert(self, collection_name: str, data: List[Dict]):
        collection = self.get_collection(collection_name)
        collection.insert(data)
        collection.flush()

    def search(self, collection_name: str, query_vector: List[float], limit: int = 5):
        collection = self.get_collection(collection_name)
        results = collection.search(
            data=[query_vector],
            anns_field="vector",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=limit,
        )
        return results

    def delete_collection(self, name: str):
        utility.drop_collection(name)
        if name in self._collections:
            del self._collections[name]

    def list_collections(self):
        return utility.list_collections()


if __name__ == "__main__":
    client = MilvusClient()
    print("Milvus client initialized")
