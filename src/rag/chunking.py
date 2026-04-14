from typing import List, Dict
import re


class TextChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        sentences = self._split_into_sentences(text)
        chunks = []
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence.split())

            if current_size + sentence_size > self.chunk_size and current_chunk:
                chunks.append(
                    {"text": " ".join(current_chunk), "metadata": metadata or {}}
                )
                keep_count = min(self.overlap // 5, len(current_chunk))
                current_chunk = current_chunk[-keep_count:] if keep_count > 0 else []
                current_size = sum(len(s.split()) for s in current_chunk)

            current_chunk.append(sentence)
            current_size += sentence_size

        if current_chunk:
            chunks.append({"text": " ".join(current_chunk), "metadata": metadata or {}})

        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
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

    def chunk_by_paragraphs(self, text: str, metadata: Dict = None) -> List[Dict]:
        paragraphs = text.split("\n\n")
        chunks = []

        for i, para in enumerate(paragraphs):
            para = para.strip()
            if para:
                chunks.append({"text": para, "metadata": (metadata or {}).copy()})
                chunks[-1]["metadata"]["chunk_index"] = i

        return chunks

    def chunk_by_tokens(self, text: str, metadata: Dict = None) -> List[Dict]:
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i : i + self.chunk_size]
            chunks.append(
                {"text": " ".join(chunk_words), "metadata": (metadata or {}).copy()}
            )
            chunks[-1]["metadata"]["chunk_start"] = i
            chunks[-1]["metadata"]["chunk_end"] = min(i + self.chunk_size, len(words))

        return chunks


if __name__ == "__main__":
    chunker = TextChunker(chunk_size=100, overlap=20)
    sample_text = "This is a sample text. It contains multiple sentences. We want to chunk this into smaller pieces."
    chunks = chunker.chunk_text(sample_text)
    print(f"Created {len(chunks)} chunks")
