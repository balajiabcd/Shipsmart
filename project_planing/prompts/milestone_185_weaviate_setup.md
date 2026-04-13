# Milestone #185: Set Up Weaviate

**Your Role:** AI/LLM Engineer

Configure Weaviate:

```bash
pip install weaviate-client
```

Create client:

```python
# src/rag/weaviate_client.py
import weaviate
import os

class WeaviateClient:
    def __init__(self, url: str = None):
        self.client = weaviate.Client(
            url=url or os.getenv("WEAVIATE_URL", "http://localhost:8080")
        )
    
    def create_schema(self, class_name: str, schema: dict):
        schema = {
            "class": class_name,
            "description": schema.get("description", ""),
            "vectorizer": schema.get("vectorizer", "text2vec-transformers"),
            "moduleConfig": {
                "text2vec-transformers": {"vectorizeClassName": False}
            }
        }
        self.client.schema.create_class(schema)
    
    def add_objects(self, class_name: str, objects: list):
        with self.client.batch as batch:
            for obj in objects:
                batch.add_data_object(obj, class_name)
    
    def query(self, class_name: str, query: str, limit: int = 5):
        return self.client.query.get(class_name).with_limit(limit).do()
```

For Docker: `docker run -p 8080:8080 -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true semitechnologies/weaviate`. Commit.