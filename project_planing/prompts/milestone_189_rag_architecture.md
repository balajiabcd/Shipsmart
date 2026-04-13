# Milestone #189: Create RAG Pipeline Architecture

**Your Role:** AI/LLM Engineer

Design retrieval system:

```python
# src/rag/pipeline.py

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import asyncio

class BaseVectorDB(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Dict]): pass
    
    @abstractmethod
    def search(self, query: str, top_k: int) -> List[Dict]: pass

class RAGPipeline:
    def __init__(self, embedding_model, vector_dbs: List[BaseVectorDB]):
        self.embedding_model = embedding_model
        self.vector_dbs = vector_dbs
    
    async def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        # Generate query embedding
        query_embedding = await self.embedding_model.embed(query)
        
        # Search all vector DBs
        results = []
        for db in self.vector_dbs:
            db_results = db.search(query_embedding, top_k)
            results.extend(db_results)
        
        # Deduplicate and rerank
        return self._dedupe_and_rerank(results, top_k)
    
    async def add_documents(self, documents: List[Dict]):
        # Generate embeddings
        texts = [doc["text"] for doc in documents]
        embeddings = await self.embedding_model.embed_batch(texts)
        
        # Add to all vector DBs
        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            doc["embedding"] = emb
            for db in self.vector_dbs:
                db.add_documents([doc])
    
    def _dedupe_and_rerank(self, results: List[Dict], top_k: int) -> List[Dict]:
        seen = set()
        deduped = []
        for r in results:
            if r["id"] not in seen:
                seen.add(r["id"])
                deduped.append(r)
        
        return sorted(deduped, key=lambda x: x["score"], reverse=True)[:top_k]
```

Commit.