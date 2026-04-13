# Milestone #196: Implement Reranking

**Your Role:** AI/LLM Engineer

Reorder retrieval results:

```python
# src/rag/reranker.py

from typing import List, Dict

class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model_name)
    
    def rerank(self, query: str, results: List[Dict], top_k: int = 5) -> List[Dict]:
        if not results:
            return []
        
        # Create pairs for scoring
        pairs = [(query, r["text"]) for r in results]
        
        # Score all pairs
        scores = self.model.predict(pairs)
        
        # Add scores and sort
        for r, score in zip(results, scores):
            rerank_score = float(score)
            r["rerank_score"] = rerank_score
            r["original_score"] = r.get("score", 0)
            r["final_score"] = (rerank_score + r["original_score"]) / 2
        
        return sorted(results, key=lambda x: x["final_score"], reverse=True)[:top_k]


class LLM Reranker:
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def rerank(self, query: str, results: List[Dict], top_k: int = 5) -> List[Dict]:
        if len(results) <= top_k:
            return results
        
        # Use LLM to score relevance
        prompt = f"""Given query: "{query}"

Rank these documents by relevance (1-10):
{chr(10).join([f"{i+1}. {r['text'][:200]}" for i, r in enumerate(results)])}

Return JSON with scores: [{"doc_id": "id", "score": 0-10}]"""
        
        response = await self.llm.generate(prompt)
        # Parse and apply scores...
        
        return results[:top_k]  # Simplified
```

Commit.