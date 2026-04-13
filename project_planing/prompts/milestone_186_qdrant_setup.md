# Milestone #186: Set Up Qdrant

**Your Role:** AI/LLM Engineer

Configure Qdrant vector search:

```bash
pip install qdrant-client
```

Create client:

```python
# src/rag/qdrant_client.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os

class QdrantClientWrapper:
    def __init__(self, url: str = None, api_key: str = None):
        self.client = QdrantClient(
            url=url or os.getenv("QDRANT_URL", "localhost"),
            api_key=api_key or os.getenv("QDRANT_API_KEY")
        )
    
    def create_collection(self, name: str, vector_size: int = 1536):
        self.client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
    
    def upsert(self, collection_name: str, points: list):
        self.client.upsert(
            collection_name=collection_name,
            points=points
        )
    
    def search(self, collection_name: str, query_vector: list, limit: int = 5):
        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )
```

Docker: `docker run -p 6333:6333 qdrant/qdrant`. Commit.