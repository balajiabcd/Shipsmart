# Milestone #191: Generate Embeddings (OpenAI)

**Your Role:** AI/LLM Engineer

Create OpenAI embeddings:

```python
# src/rag/embeddings_openai.py

from openai import OpenAI
import os
import numpy as np
from typing import List

class OpenAIEmbeddings:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.dimension = 1536  # text-embedding-3-small
    
    def embed(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return np.array(response.data[0].embedding)
    
    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[np.ndarray]:
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            response = self.client.embeddings.create(
                model=self.model,
                input=batch
            )
            all_embeddings.extend([np.array(d.embedding) for d in response.data])
        
        return all_embeddings
    
    async def aembed(self, text: str) -> np.ndarray:
        return self.embed(text)
```

Test:
```python
emb = OpenAIEmbeddings()
vector = emb.embed("Shipsmart delivery delay prediction")
print(f"Embedding dimension: {len(vector)}")
```

Commit.