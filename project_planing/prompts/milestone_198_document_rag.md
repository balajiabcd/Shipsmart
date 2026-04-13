# Milestone #198: Document RAG Pipeline

**Your Role:** AI/LLM Engineer

Write RAG documentation:

```markdown
# Shipsmart RAG Pipeline

## Overview

Retrieval-Augmented Generation (RAG) system for contextual delivery information.

## Vector Databases

| Database | Use Case | Status |
|----------|----------|--------|
| ChromaDB | Local dev | ✅ |
| Pinecone | Cloud production | ✅ |
| Weaviate | Self-hosted | ✅ |
| Qdrant | High performance | ✅ |
| Milvus | Scale workloads | ✅ |
| FAISS | Offline/fast | ✅ |

## Architecture

1. **Embedding Generation**
   - OpenAI: text-embedding-3-small (1536 dim)
   - HuggingFace: all-MiniLM-L6-v2 (384 dim)

2. **Chunking** (`src/rag/chunking.py`)
   - Sentence-based splitting
   - 512 tokens chunk size
   - 50 token overlap

3. **Retrieval** (`src/rag/retriever.py`)
   - Query processing
   - Multi-DB retrieval
   - Result deduplication

4. **Hybrid Search** (`src/rag/hybrid_search.py`)
   - Vector + keyword combination
   - Configurable alpha weight

5. **Reranking** (`src/rag/reranker.py`)
   - Cross-encoder scoring
   - LLM-based reranking

6. **Caching** (`src/rag/cache.py`)
   - LRU in-memory cache
   - Redis for production

## API Endpoints

- POST /rag/query - Query the RAG system
- POST /rag/index - Add documents
- GET /rag/status - Check indexing status
```

Save to `docs/rag_pipeline.md`. Commit.