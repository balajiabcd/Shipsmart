from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
import numpy as np


class BaseVectorDB(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Dict]) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int) -> List[Dict]:
        pass


class EmbeddingModel(ABC):
    @abstractmethod
    def embed(self, text: str) -> np.ndarray:
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        pass


class RAGPipeline:
    def __init__(
        self, embedding_model: EmbeddingModel, vector_dbs: List[BaseVectorDB] = None
    ):
        self.embedding_model = embedding_model
        self.vector_dbs = vector_dbs or []

    def add_vector_db(self, db: BaseVectorDB):
        self.vector_dbs.append(db)

    async def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        query_embedding = self.embedding_model.embed(query).tolist()

        results = []
        for db in self.vector_dbs:
            db_results = db.search(query_embedding, top_k)
            results.extend(db_results)

        return self._dedupe_and_rerank(results, top_k)

    async def add_documents(self, documents: List[Dict]):
        texts = [doc["text"] for doc in documents]
        embeddings = self.embedding_model.embed_batch(texts)

        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            doc["embedding"] = emb.tolist()
            for db in self.vector_dbs:
                db.add_documents([doc])

    def _dedupe_and_rerank(self, results: List[Dict], top_k: int) -> List[Dict]:
        seen = set()
        deduped = []
        for r in results:
            doc_id = r.get("doc_id") or r.get("id")
            if doc_id and doc_id not in seen:
                seen.add(doc_id)
                deduped.append(r)

        return sorted(deduped, key=lambda x: x.get("score", 0), reverse=True)[:top_k]


class ChromaDBAdapter(BaseVectorDB):
    def __init__(self, chroma_client, collection_name: str):
        self.client = chroma_client
        self.collection_name = collection_name

    def add_documents(self, documents: List[Dict]) -> None:
        ids = [doc.get("doc_id", f"doc_{i}") for i, doc in enumerate(documents)]
        texts = [doc.get("text", "") for doc in documents]
        embeddings = [doc.get("embedding", []) for doc in documents]
        metadata = [doc.get("metadata", {}) for doc in documents]

        self.client.add_documents(
            self.collection_name,
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadata=metadata,
        )

    def search(self, query_embedding: List[float], top_k: int) -> List[Dict]:
        results = self.client.query(self.collection_name, query_embedding, top_k)

        parsed = []
        for i in range(len(results.get("documents", [[]])[0])):
            parsed.append(
                {
                    "doc_id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "score": results["distances"][0][i]
                    if "distances" in results
                    else 0,
                    "metadata": results["metadatas"][0][i]
                    if "metadatas" in results
                    else {},
                }
            )
        return parsed


class FAISSAdapter(BaseVectorDB):
    def __init__(self, faiss_client):
        self.client = faiss_client

    def add_documents(self, documents: List[Dict]) -> None:
        texts = [doc.get("text", "") for doc in documents]
        embeddings = np.array([doc.get("embedding", []) for doc in documents])
        doc_ids = [doc.get("doc_id", f"doc_{i}") for i, doc in enumerate(documents)]

        self.client.add_vectors(embeddings, doc_ids, texts)

    def search(self, query_embedding: List[float], top_k: int) -> List[Dict]:
        results = self.client.search(np.array(query_embedding), top_k)
        return results


if __name__ == "__main__":
    print("RAG Pipeline ready")
