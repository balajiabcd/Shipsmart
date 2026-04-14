from typing import List, Dict, Optional
import numpy as np


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self.model = None

    def _load_model(self):
        if self.model is None:
            from sentence_transformers import CrossEncoder

            self.model = CrossEncoder(self.model_name)

    def rerank(self, query: str, results: List[Dict], top_k: int = 5) -> List[Dict]:
        if not results:
            return []

        self._load_model()

        pairs = [(query, r.get("text", "")) for r in results]

        scores = self.model.predict(pairs)

        for r, score in zip(results, scores):
            rerank_score = float(score)
            r["rerank_score"] = rerank_score
            r["original_score"] = r.get("score", r.get("distance", 0))
            r["final_score"] = (rerank_score + r["original_score"]) / 2

        return sorted(results, key=lambda x: x["final_score"], reverse=True)[:top_k]


class LLMReranker:
    def __init__(self, llm_client):
        self.llm = llm_client

    async def rerank(
        self, query: str, results: List[Dict], top_k: int = 5
    ) -> List[Dict]:
        if len(results) <= top_k:
            return results

        prompt = f"""Given query: "{query}"

Rank these documents by relevance (1-10):
{chr(10).join([f"{i + 1}. {r.get('text', '')[:200]}" for i, r in enumerate(results)])}

Return JSON with scores: [{{"doc_id": "id", "score": 0-10}}]"""

        response = await self.llm.generate(prompt)

        return results[:top_k]


class SimpleReranker:
    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha

    def rerank(self, query: str, results: List[Dict], top_k: int = 5) -> List[Dict]:
        if not results:
            return []

        for r in results:
            original = r.get("score", r.get("distance", 0))
            text = r.get("text", "")

            query_terms = set(query.lower().split())
            text_terms = set(text.lower().split())

            overlap = len(query_terms & text_terms) / max(len(query_terms), 1)

            r["final_score"] = self.alpha * original + (1 - self.alpha) * overlap

        return sorted(results, key=lambda x: x.get("final_score", 0), reverse=True)[
            :top_k
        ]


class ReciprocalRankReranker:
    def __init__(self, k: int = 60):
        self.k = k

    def rerank(self, results_lists: List[List[Dict]], top_k: int = 5) -> List[Dict]:
        scores = {}

        for results in results_lists:
            for i, r in enumerate(results):
                doc_id = r.get("doc_id") or r.get("id")
                if doc_id not in scores:
                    scores[doc_id] = {"data": r, "score": 0}
                scores[doc_id]["score"] += 1 / (i + 1)

        sorted_results = sorted(scores.values(), key=lambda x: x["score"], reverse=True)

        return [r["data"] for r in sorted_results[:top_k]]


if __name__ == "__main__":
    print("Reranker classes defined")
