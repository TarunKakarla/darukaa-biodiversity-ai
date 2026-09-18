import os
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader


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

        # Persistent Chroma database
        self.client = chromadb.PersistentClient(
            path=self.persist_dir
        )

        self.collection = self.client.get_or_create_collection(
            "environmental_sources"
        )

        # Load embedding model once
        self.embedder = SentenceTransformer(
            self.embedding_model_name
        )

    def _chunks(self, text, size=900, overlap=150):
        words = text.split()
        step = max(1, size - overlap)

        for i in range(0, len(words), step):
            chunk = " ".join(
                words[i:i + size]
            ).strip()

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
        chunks = list(self._chunks(text))

        if not chunks:
            return 0

        ids = [
            f"{document_id}-{i}"
            for i in range(len(chunks))
        ]

        embeddings = self.embedder.encode(
            chunks,
            normalize_embeddings=True
        ).tolist()

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

        # Upsert makes repeated ingestion safe:
        # same document_id + chunk number = same Chroma ID
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
        reader = PdfReader(path)

        total_chunks = 0

        # Process each page separately so we retain
        # the original PDF page number.
        for page_index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if not text.strip():
                continue

            chunks = list(self._chunks(text))

            if not chunks:
                continue

            ids = [
                f"{document_id}-p{page_index}-c{i}"
                for i in range(len(chunks))
            ]

            embeddings = self.embedder.encode(
                chunks,
                normalize_embeddings=True
            ).tolist()

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
                print(
                    f"  Processed page {page_index}/{len(reader.pages)} "
                    f"({total_chunks} chunks)"
                )

        return total_chunks

    def retrieve(self, query, k=5):
        # Don't query an empty collection
        if self.collection.count() == 0:
            return []

        emb = self.embedder.encode(
            [query],
            normalize_embeddings=True
        ).tolist()

        r = self.collection.query(
            query_embeddings=emb,
            n_results=min(k, self.collection.count())
        )

        results = []

        if not r.get("documents") or not r["documents"][0]:
            return results

        for i, doc in enumerate(r["documents"][0]):
            results.append(
                {
                    "text": doc,
                    "metadata": r["metadatas"][0][i],
                    "distance": (
                        r["distances"][0][i]
                        if r.get("distances")
                        else None
                    )
                }
            )

        return results


# ---------------------------------------------------------
# Shared RAG store
# ---------------------------------------------------------
#
# The embedding model is loaded once when the application
# imports this module.
#
rag_store = RAGStore()