import weaviate
import os
from typing import List, Dict, Optional


class WeaviateClient:
    def __init__(self, url: str = None):
        self.client = weaviate.Client(
            url=url or os.getenv("WEAVIATE_URL", "http://localhost:8080")
        )

    def create_schema(
        self,
        class_name: str,
        description: str = "",
        vectorizer: str = "text2vec-transformers",
    ):
        schema = {
            "class": class_name,
            "description": description,
            "vectorizer": vectorizer,
            "moduleConfig": {"text2vec-transformers": {"vectorizeClassName": False}},
        }
        self.client.schema.create_class(schema)

    def add_objects(self, class_name: str, objects: List[Dict]):
        with self.client.batch as batch:
            for obj in objects:
                batch.add_data_object(obj, class_name)

    def query(self, class_name: str, query: str, limit: int = 5):
        return (
            self.client.query.get(class_name)
            .with_limit(limit)
            .with_additional(["certainty"])
            .do()
        )

    def delete_class(self, class_name: str):
        self.client.schema.delete_class(class_name)

    def get_schema(self):
        return self.client.schema.get()


if __name__ == "__main__":
    client = WeaviateClient()
    print("Weaviate client initialized")
