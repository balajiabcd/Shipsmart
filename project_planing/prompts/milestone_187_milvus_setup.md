# Milestone #187: Set Up Milvus

**Your Role:** AI/LLM Engineer

Configure Milvus vector database:

```bash
pip install pymilvus
```

Create client:

```python
# src/rag/milvus_client.py
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

class MilvusClient:
    def __init__(self, host: str = "localhost", port: str = "19530"):
        connections.connect(host=host, port=port)
    
    def create_collection(self, name: str, dimension: int = 1536):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
        ]
        schema = CollectionSchema(fields, description=f"{name} collection")
        collection = Collection(name, schema)
        
        # Create index
        index_params = {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}}
        collection.create_index("vector", index_params)
        
        return collection
    
    def insert(self, collection_name: str, data: list):
        collection = Collection(collection_name)
        collection.insert(data)
        collection.flush()
    
    def search(self, collection_name: str, query_vector: list, limit: int = 5):
        collection = Collection(collection_name)
        results = collection.search(
            data=[query_vector],
            anns_field="vector",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=limit
        )
        return results
```

Docker: `docker run -p 19530:19530 milvusdb/milvus`. Commit.