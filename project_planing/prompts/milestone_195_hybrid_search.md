# Milestone #195: Create Hybrid Search

**Your Role:** AI/LLM Engineer

Combine vector + keyword search:

```python
# src/rag/hybrid_search.py

from typing import List, Dict
import re
from collections import defaultdict

class HybridSearch:
    def __init__(self, vector_retriever, keyword_index):
        self.vector_retriever = vector_retriever
        self.keyword_index = keyword_index
    
    async def search(self, query: str, top_k: int = 10, alpha: float = 0.5) -> List[Dict]:
        """Combine vector and keyword search
        
        alpha: weight for vector (1-alpha) for keyword
        """
        # Vector search
        vector_results = await self.vector_retriever.retrieve(query, top_k * 2)
        
        # Keyword search
        keyword_results = self.keyword_index.search(query, top_k * 2)
        
        # Normalize scores
        vector_scores = self._normalize_scores([r["score"] for r in vector_results])
        keyword_scores = self._normalize_scores([r["score"] for r in keyword_results])
        
        # Combine
        combined = defaultdict(lambda: {"score": 0, "data": None})
        
        for r, score in zip(vector_results, vector_scores):
            doc_id = r["id"]
            combined[doc_id]["score"] += alpha * score
            combined[doc_id]["data"] = r
        
        for r, score in zip(keyword_results, keyword_scores):
            doc_id = r["id"]
            combined[doc_id]["score"] += (1 - alpha) * score
            if combined[doc_id]["data"] is None:
                combined[doc_id]["data"] = r
        
        # Sort and return
        sorted_results = sorted(combined.values(), key=lambda x: x["score"], reverse=True)
        return [r["data"] for r in sorted_results[:top_k]]
    
    def _normalize_scores(self, scores: List[float]) -> List[float]:
        if not scores:
            return []
        min_s, max_s = min(scores), max(scores)
        if max_s == min_s:
            return [1.0] * len(scores)
        return [(s - min_s) / (max_s - min_s) for s in scores]

class KeywordIndex:
    def __init__(self):
        self.index = defaultdict(list)
    
    def add(self, doc_id: str, text: str):
        tokens = re.findall(r'\w+', text.lower())
        for token in set(tokens):
            self.index[token].append(doc_id)
    
    def search(self, query: str, top_k: int) -> List[Dict]:
        tokens = re.findall(r'\w+', query.lower())
        scores = defaultdict(float)
        
        for token in tokens:
            for doc_id in self.index[token]:
                scores[doc_id] += 1
        
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{"id": doc_id, "score": score} for doc_id, score in sorted_docs[:top_k]]
```

Commit.