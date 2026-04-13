# Milestone #192: Generate Embeddings (HuggingFace)

**Your Role:** AI/LLM Engineer

Use sentence transformers:

```bash
pip install sentence-transformers
```

Create embeddings:

```python
# src/rag/embeddings_huggingface.py

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class HuggingFaceEmbeddings:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def embed(self, text: str) -> np.ndarray:
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_batch(self, texts: List[str], batch_size: int = 32, show_progress: bool = True) -> List[np.ndarray]:
        return self.model.encode(
            texts, 
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
    
    async def aembed(self, text: str) -> np.ndarray:
        return self.embed(text)
```

Test:
```python
emb = HuggingFaceEmbeddings()
vector = emb.embed("Shipsmart delivery delay prediction")
print(f"Embedding dimension: {len(vector)}")
```

Models to consider:
- `all-mpnet-base-v2` (768 dim, higher quality)
- `all-MiniLM-L6-v2` (384 dim, faster)
- `multi-qa-mpnet-base-v2` (good for QA)

Commit.