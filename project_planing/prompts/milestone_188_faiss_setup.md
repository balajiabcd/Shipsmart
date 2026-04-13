# Milestone #188: Set Up FAISS

**Your Role:** AI/LLM Engineer

Configure FAISS vector library:

```bash
pip install faiss-cpu  # or faiss-gpu for GPU support
```

Create client:

```python
# src/rag/faiss_client.py
import faiss
import numpy as np

class FAISSClient:
    def __init__(self, dimension: int = 1536, use_gpu: bool = False):
        self.dimension = dimension
        self.index = None
        self.id_to_doc = {}
        self.use_gpu = use_gpu
    
    def create_index(self, metric: str = "L2"):
        if metric == "L2":
            self.index = faiss.IndexFlatL2(self.dimension)
        elif metric == "IP":  # Inner product
            self.index = faiss.IndexFlatIP(self.dimension)
        
        if self.use_gpu:
            self.index = faiss.index_gpu_to_cpu(self.index)
    
    def add_vectors(self, vectors: np.ndarray, doc_ids: list):
        vectors = np.array(vectors).astype('float32')
        self.index.add(vectors)
        self.id_to_doc.update({i: doc_ids[i] for i in range(len(doc_ids))})
    
    def search(self, query_vector: np.ndarray, k: int = 5):
        query = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.id_to_doc):
                results.append({
                    "doc_id": self.id_to_doc[idx],
                    "distance": float(dist)
                })
        return results
    
    def save_index(self, path: str):
        faiss.write_index(self.index, f"{path}.index")
    
    def load_index(self, path: str):
        self.index = faiss.read_index(f"{path}.index")
```

Commit.