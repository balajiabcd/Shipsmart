import os
import numpy as np
from typing import List, Optional


class OllamaEmbeddings:
    def __init__(self, model: str = None):
        from src.llm.ollama_client import OllamaClient

        self.client = OllamaClient(
            model=model or os.getenv("OLLAMA_ACTIVE_MODEL", "phi:2.7b")
        )
        self.model = self.client.model
        self._dimension = None

    def embed(self, text: str) -> np.ndarray:
        embedding = self.client.embed(text)
        return np.array(embedding, dtype=np.float32)

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[np.ndarray]:
        return [self.embed(text) for text in texts]

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            try:
                test_emb = self.embed("test")
                self._dimension = len(test_emb)
            except:
                self._dimension = 4096
        return self._dimension


class HuggingFaceEmbeddings:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._dimension = 384

    def _load_model(self):
        if self.model is None:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(self.model_name)
            self._dimension = self.model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> np.ndarray:
        self._load_model()
        return self.model.encode(text, convert_to_numpy=True)

    def embed_batch(
        self, texts: List[str], batch_size: int = 32, show_progress: bool = False
    ) -> List[np.ndarray]:
        self._load_model()
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
        )
        return [emb for emb in embeddings]

    @property
    def dimension(self) -> int:
        if self.model is None:
            self._load_model()
        return self._dimension


class DummyEmbeddings:
    def __init__(self, dimension: int = 4096):
        self._dimension = dimension

    def embed(self, text: str) -> np.ndarray:
        return np.random.randn(self._dimension).astype(np.float32)

    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        return [self.embed(t) for t in texts]

    @property
    def dimension(self) -> int:
        return self._dimension


if __name__ == "__main__":
    print("Embedding classes ready (Ollama, HuggingFace, Dummy)")
