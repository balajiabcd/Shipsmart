# Milestone #184: Set Up Pinecone

**Your Role:** AI/LLM Engineer

Configure Pinecone cloud vector DB:

```bash
pip install pinecone-client
```

Add to `.env`:
```bash
PINECONE_API_KEY=your-api-key
PINECONE_ENVIRONMENT=us-east-1
```

Create client:

```python
# src/rag/pinecone_client.py
import pinecone
import os

class PineconeClient:
    def __init__(self):
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENVIRONMENT")
        )
    
    def create_index(self, name: str, dimension: int = 1536, metric: str = "cosine"):
        if name not in pinecone.list_indexes():
            pinecone.create_index(
                name=name,
                dimension=dimension,
                metric=metric
            )
        return pinecone.Index(name)
    
    def upsert_vectors(self, index_name: str, vectors: list):
        index = pinecone.Index(index_name)
        index.upsert(vectors=vectors)
    
    def query(self, index_name: str, query_vector: list, top_k: int = 5):
        index = pinecone.Index(index_name)
        return index.query(vector=query_vector, top_k=top_k)
    
    def delete_index(self, name: str):
        pinecone.delete_index(name)
```

Test:
```python
client = PineconeClient()
idx = client.create_index("shipsmart", dimension=1536)
print("Pinecone connected")
```

Commit.