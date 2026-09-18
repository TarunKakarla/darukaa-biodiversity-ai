"""
Darukaa.Earth - RAG Bootstrap

Used during deployment to prepare the Chroma vector database.

If Chroma already contains documents, nothing is re-ingested.

If Chroma is empty:
1. Download the registered environmental PDFs.
2. Store them in data/sources/
3. Run the existing ingestion pipeline.
"""

import urllib.request
from pathlib import Path

from app.rag.store import RAGStore
from scripts.ingest_sources import SOURCES, main as ingest_main


def download_file(url, destination):
    print(f"Downloading: {url}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    urllib.request.urlretrieve(url, destination)

    size_mb = destination.stat().st_size / (1024 * 1024)

    print(f"Downloaded: {size_mb:.1f} MB")


def main():

    project_root = Path(__file__).resolve().parents[1]
    sources_dir = project_root / "data" / "sources"

    print("=" * 60)
    print("DARUKAA.EARTH - RAG BOOTSTRAP")
    print("=" * 60)

    store = RAGStore()

    current_count = store.collection.count()

    print(f"\nCurrent Chroma chunks: {current_count}")

    # -----------------------------------------------------
    # If embeddings already exist, do nothing.
    # -----------------------------------------------------

    if current_count > 0:
        print("\nRAG database already exists.")
        print("Skipping PDF download and ingestion.")
        print("=" * 60)
        return

    print("\nChroma is empty.")
    print("Preparing source documents...")

    sources_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------
    # Download missing PDFs
    # -----------------------------------------------------

    for filename, (title, url, document_id) in SOURCES.items():

        pdf_path = sources_dir / filename

        print("\n" + "-" * 60)
        print(f"Source: {title}")

        if pdf_path.exists():
            print("PDF already exists.")
            continue

        try:
            download_file(url, pdf_path)

        except Exception as e:
            print(f"ERROR downloading {filename}: {e}")
            raise

    # -----------------------------------------------------
    # Run existing ingestion pipeline
    # -----------------------------------------------------

    print("\nStarting PDF ingestion...")

    ingest_main()

    # -----------------------------------------------------
    # Final verification
    # -----------------------------------------------------

    final_store = RAGStore()

    final_count = final_store.collection.count()

    print("\n" + "=" * 60)
    print("RAG BOOTSTRAP COMPLETE")
    print("=" * 60)

    print(f"Total Chroma chunks: {final_count}")

    if final_count == 0:
        raise RuntimeError(
            "RAG bootstrap finished but no chunks were created."
        )


if __name__ == "__main__":
    main()
