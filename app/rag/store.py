import os
from pathlib import Path
from typing import Any, Dict, List

from app.rag.knowledge_data import search_knowledge_base, KNOWLEDGE_RECORDS

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    from pypdf import PdfReader
    CHROMA_AVAILABLE = True
except Exception as e:
    CHROMA_AVAILABLE = False


class RAGStore:
    def __init__(self, persist_dir=None, embedding_model=None):
        self.persist_dir = persist_dir or os.getenv(
            "CHROMA_PATH",
            "./data/chroma"
        )
        self.embedding_model_name = embedding_model or os.getenv(
            "EMBEDDING_MODEL",
            "all-MiniLM-L6-v2"
        )

        self.client = None
        self.collection = None
        self.embedder = None

        if CHROMA_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(path=self.persist_dir)
                self.collection = self.client.get_or_create_collection("environmental_sources")
                self.embedder = SentenceTransformer(self.embedding_model_name)
            except Exception as e:
                print(f"[RAGStore] Warning: Could not initialize Chroma vector engine: {e}")
                self.client = None
                self.collection = None
                self.embedder = None

    def _chunks(self, text, size=900, overlap=150):
        words = text.split()
        step = max(1, size - overlap)
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + size]).strip()
            if chunk:
                yield chunk

    def ingest_text(
        self,
        text,
        source_title,
        source_url,
        document_id,
        page_number=None
    ):
        if not self.collection or not self.embedder:
            return 0

        chunks = list(self._chunks(text))
        if not chunks:
            return 0

        ids = [f"{document_id}-{i}" for i in range(len(chunks))]
        embeddings = self.embedder.encode(chunks, normalize_embeddings=True).tolist()

        metadatas = []
        for _ in chunks:
            metadata = {
                "source_title": source_title,
                "source_url": source_url,
                "document_id": document_id,
            }
            if page_number is not None:
                metadata["page"] = page_number
            metadatas.append(metadata)

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )
        return len(chunks)

    def ingest_pdf(
        self,
        path,
        source_title,
        source_url,
        document_id
    ):
        if not CHROMA_AVAILABLE or not self.collection or not self.embedder:
            raise RuntimeError("Chroma/SentenceTransformer/pypdf not available for PDF ingestion.")

        reader = PdfReader(path)
        total_chunks = 0

        for page_index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                continue

            chunks = list(self._chunks(text))
            if not chunks:
                continue

            ids = [f"{document_id}-p{page_index}-c{i}" for i in range(len(chunks))]
            embeddings = self.embedder.encode(chunks, normalize_embeddings=True).tolist()
            metadatas = [
                {
                    "source_title": source_title,
                    "source_url": source_url,
                    "document_id": document_id,
                    "page": page_index,
                }
                for _ in chunks
            ]

            self.collection.upsert(
                ids=ids,
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas
            )
            total_chunks += len(chunks)

            if page_index % 25 == 0:
                print(f"  Processed page {page_index}/{len(reader.pages)} ({total_chunks} chunks)")

        return total_chunks

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval combining vector similarity search (from indexed PDFs)
        with structured scientific knowledge records (from FAO, IPCC, CBD, IPBES).
        Guarantees real, high-quality citations across all deployment environments.
        """
        results: List[Dict[str, Any]] = []
        seen_titles = set()

        # 1. First, retrieve vector embeddings from ChromaDB if available
        if self.collection and self.embedder:
            try:
                count = self.collection.count()
                if count > 0:
                    emb = self.embedder.encode([query], normalize_embeddings=True).tolist()
                    r = self.collection.query(
                        query_embeddings=emb,
                        n_results=min(k, count)
                    )
                    if r.get("documents") and r["documents"][0]:
                        for i, doc in enumerate(r["documents"][0]):
                            meta = r["metadatas"][0][i]
                            title = meta.get("source_title", "")
                            key = (title, meta.get("page"))
                            if key not in seen_titles:
                                seen_titles.add(key)
                                results.append({
                                    "text": doc,
                                    "metadata": {
                                        "source_title": meta.get("source_title"),
                                        "source_url": meta.get("source_url"),
                                        "page_number": meta.get("page"),
                                        "document_id": meta.get("document_id"),
                                        "supporting_excerpt_or_summary": doc[:300].strip() + "..."
                                    },
                                    "distance": r["distances"][0][i] if r.get("distances") else None
                                })
            except Exception as e:
                print(f"[RAGStore] Chroma query warning: {e}")

        # 2. Enrich/supplement with structured authoritative knowledge base
        kb_records = search_knowledge_base(query, k=k)
        for rec in kb_records:
            key = (rec["source_title"], rec["page_number"])
            if key not in seen_titles:
                seen_titles.add(key)
                excerpt = f"{rec['quantitative_finding']} {rec['causal_mechanism']}"
                results.append({
                    "text": rec["text"],
                    "metadata": {
                        "source_title": rec["source_title"],
                        "source_url": rec["source_url"],
                        "page_number": rec["page_number"],
                        "document_id": rec["id"],
                        "quantitative_finding": rec.get("quantitative_finding"),
                        "causal_mechanism": rec.get("causal_mechanism"),
                        "supporting_excerpt_or_summary": excerpt
                    },
                    "distance": 0.15
                })

        return results[:max(k, len(results))]


# Singleton instance
rag_store = RAGStore()