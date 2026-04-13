# Milestone #190: Create Document Chunking Logic

**Your Role:** AI/LLM Engineer

Split data for embedding:

```python
# src/rag/chunking.py

from typing import List, Dict
import re

class TextChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, metadata: dict = None) -> List[Dict]:
        sentences = self._split_into_sentences(text)
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence.split())
            
            if current_size + sentence_size > self.chunk_size and current_chunk:
                chunks.append({
                    "text": " ".join(current_chunk),
                    "metadata": metadata or {}
                })
                # Keep overlap
                current_chunk = current_chunk[-self.overlap//5:] if len(current_chunk) > 5 else []
                current_size = sum(len(s.split()) for s in current_chunk)
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        if current_chunk:
            chunks.append({"text": " ".join(current_chunk), "metadata": metadata or {}})
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        # Split on sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        all_chunks = []
        for doc in documents:
            text = doc.get("text", "")
            metadata = {k: v for k, v in doc.items() if k != "text"}
            chunks = self.chunk_text(text, metadata)
            for i, chunk in enumerate(chunks):
                chunk["chunk_id"] = f"{doc.get('id', 'doc')}_{i}"
            all_chunks.extend(chunks)
        return all_chunks
```

Commit.