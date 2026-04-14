from typing import List, Dict
import re
from collections import defaultdict


class HybridSearch:
    def __init__(self, vector_retriever, keyword_index=None):
        self.vector_retriever = vector_retriever
        self.keyword_index = keyword_index or KeywordIndex()

    async def search(
        self, query: str, top_k: int = 10, alpha: float = 0.5
    ) -> List[Dict]:
        vector_results = await self.vector_retriever.retrieve(query, top_k * 2)

        if self.keyword_index.index:
            keyword_results = self.keyword_index.search(query, top_k * 2)
        else:
            keyword_results = []

        vector_scores = self._normalize_scores(
            [r.get("score", r.get("distance", 1)) for r in vector_results]
        )
        keyword_scores = (
            self._normalize_scores([r["score"] for r in keyword_results])
            if keyword_results
            else []
        )

        combined = defaultdict(lambda: {"score": 0, "data": None})

        for r, score in zip(vector_results, vector_scores):
            doc_id = r.get("doc_id") or r.get("id") or f"vec_{id(r)}"
            combined[doc_id]["score"] += alpha * score
            combined[doc_id]["data"] = r

        for r, score in zip(keyword_results, keyword_scores):
            doc_id = r["id"]
            combined[doc_id]["score"] += (1 - alpha) * score
            if combined[doc_id]["data"] is None:
                combined[doc_id]["data"] = r

        sorted_results = sorted(
            combined.values(), key=lambda x: x["score"], reverse=True
        )
        return [r["data"] for r in sorted_results[:top_k] if r["data"] is not None]

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
        self.documents = {}

    def add(self, doc_id: str, text: str):
        tokens = re.findall(r"\w+", text.lower())
        for token in set(tokens):
            self.index[token].append(doc_id)
        self.documents[doc_id] = text

    def search(self, query: str, top_k: int) -> List[Dict]:
        tokens = re.findall(r"\w+", query.lower())
        scores = defaultdict(float)

        for token in tokens:
            for doc_id in self.index[token]:
                scores[doc_id] += 1

        if not scores:
            return []

        max_score = max(scores.values())
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return [
            {
                "id": doc_id,
                "score": score / max_score,
                "text": self.documents.get(doc_id, ""),
            }
            for doc_id, score in sorted_docs[:top_k]
        ]

    def clear(self):
        self.index.clear()
        self.documents.clear()


class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents = {}
        self.avg_doc_len = 0
        self.doc_lengths = {}
        self.inverted_index = defaultdict(list)
        self.doc_count = 0

    def add_document(self, doc_id: str, text: str):
        tokens = re.findall(r"\w+", text.lower())
        self.documents[doc_id] = tokens
        self.doc_lengths[doc_id] = len(tokens)

        token_counts = defaultdict(int)
        for token in tokens:
            token_counts[token] += 1

        for token, count in token_counts.items():
            self.inverted_index[token].append((doc_id, count))

        self.doc_count += 1
        self.avg_doc_len = sum(self.doc_lengths.values()) / self.doc_count

    def search(self, query: str, top_k: int) -> List[Dict]:
        query_tokens = re.findall(r"\w+", query.lower())
        scores = defaultdict(float)

        for token in query_tokens:
            if token in self.inverted_index:
                doc_freq = len(self.inverted_index[token])
                idf = (self.doc_count - doc_freq + 0.5) / (doc_freq + 0.5 + 1)

                for doc_id, term_freq in self.inverted_index[token]:
                    doc_len = self.doc_lengths.get(doc_id, 1)
                    tf_norm = (term_freq * (self.k1 + 1)) / (
                        term_freq
                        + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
                    )
                    scores[doc_id] += idf * tf_norm

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        max_score = sorted_docs[0][1] if sorted_docs else 1
        return [
            {
                "id": doc_id,
                "score": score / max_score,
                "text": " ".join(self.documents.get(doc_id, [])),
            }
            for doc_id, score in sorted_docs[:top_k]
        ]


if __name__ == "__main__":
    print("Hybrid search classes defined")
