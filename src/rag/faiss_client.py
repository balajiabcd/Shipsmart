import faiss
import numpy as np
import os
from typing import List, Dict, Optional


class FAISSClient:
    def __init__(self, dimension: int = 4096, use_gpu: bool = False):
        self.dimension = dimension
        self.index = None
        self.id_to_doc = {}
        self.metadata = {}
        self.use_gpu = use_gpu
        self._next_id = 0

    def create_index(self, metric: str = "L2"):
        if metric == "L2":
            self.index = faiss.IndexFlatL2(self.dimension)
        elif metric == "IP":
            self.index = faiss.IndexFlatIP(self.dimension)

        if self.use_gpu:
            self.index = faiss.index_gpu_to_cpu(self.index)

    def add_vectors(
        self,
        vectors: np.ndarray,
        doc_ids: List[str] = None,
        texts: List[str] = None,
        metadata: List[Dict] = None,
    ):
        vectors = np.array(vectors).astype("float32")

        if doc_ids is None:
            doc_ids = [f"doc_{i}" for i in range(len(vectors))]

        start_id = self._next_id
        self.index.add(vectors)

        for i, doc_id in enumerate(doc_ids):
            self.id_to_doc[start_id + i] = doc_id
            if texts:
                self.metadata[doc_id] = {
                    "text": texts[i],
                    "metadata": metadata[i] if metadata else {},
                }

        self._next_id += len(vectors)

    def search(self, query_vector: np.ndarray, k: int = 5):
        query = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx in self.id_to_doc:
                doc_id = self.id_to_doc[idx]
                result = {
                    "doc_id": doc_id,
                    "distance": float(dist),
                    "text": self.metadata.get(doc_id, {}).get("text", ""),
                    "metadata": self.metadata.get(doc_id, {}).get("metadata", {}),
                }
                results.append(result)
        return results

    def save_index(self, path: str):
        faiss.write_index(self.index, f"{path}.index")
        import json

        with open(f"{path}_meta.json", "w") as f:
            json.dump({"id_to_doc": self.id_to_doc, "metadata": self.metadata}, f)

    def load_index(self, path: str):
        self.index = faiss.read_index(f"{path}.index")
        try:
            import json

            with open(f"{path}_meta.json", "r") as f:
                data = json.load(f)
                self.id_to_doc = data.get("id_to_doc", {})
                self.metadata = data.get("metadata", {})
        except:
            pass


if __name__ == "__main__":
    client = FAISSClient(dimension=4096)
    client.create_index("L2")
    print("FAISS client initialized")
