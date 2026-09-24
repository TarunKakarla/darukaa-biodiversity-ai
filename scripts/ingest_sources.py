"""
Darukaa.Earth - Environmental PDF Ingestion

Reads authoritative environmental PDFs from data/sources/
and stores their chunks + metadata in persistent Chroma.

Safe to run repeatedly:
- Existing document chunks are removed before re-ingestion.
- New PDFs can be added later.
- Page numbers are preserved.
"""

from pathlib import Path

from app.rag.store import RAGStore


# ---------------------------------------------------------
# Source registry
# ---------------------------------------------------------
#
# filename:
#     Exact PDF filename inside data/sources/
#
# title:
#     Official document title
#
# url:
#     Official source URL
#
# document_id:
#     Stable internal identifier
#
SOURCES = {
    "ca3129en.pdf": (
        "The State of the World's Biodiversity for Food and Agriculture",
        "https://www.fao.org/3/ca3129en/ca3129en.pdf",
        "fao_state_world_biodiversity_food_agriculture_2019",
    ),

    "gbo-5-en.pdf": (
        "Global Biodiversity Outlook 5",
        "https://www.cbd.int/gbo/gbo5/publication/gbo-5-en.pdf",
        "cbd_global_biodiversity_outlook_5",
    ),
}


# ---------------------------------------------------------
# Delete existing chunks for a document
# ---------------------------------------------------------

def delete_document(store, document_id):
    """
    Remove all existing Chroma chunks belonging to one document.

    This prevents stale chunks from remaining when a PDF is
    replaced or re-ingested.
    """

    existing = store.collection.get(
        where={"document_id": document_id},
        include=[]
    )

    ids = existing.get("ids", [])

    if ids:
        store.collection.delete(ids=ids)

    return len(ids)


# ---------------------------------------------------------
# Main ingestion
# ---------------------------------------------------------

def main():

    project_root = Path(__file__).resolve().parents[1]
    sources_dir = project_root / "data" / "sources"

    if not sources_dir.exists():
        print(f"ERROR: Sources directory does not exist:")
        print(f"  {sources_dir}")
        return

    print("=" * 60)
    print("DARUKAA.EARTH - ENVIRONMENTAL PDF INGESTION")
    print("=" * 60)

    print(f"\nSources directory:")
    print(f"  {sources_dir}")

    # Use the same persistent Chroma location as the application.
    store = RAGStore()

    print("\nCurrent Chroma chunks:")
    print(f"  {store.collection.count()}")

    total_chunks = 0

    # -----------------------------------------------------
    # Process registered sources
    # -----------------------------------------------------

    for filename, (title, url, document_id) in SOURCES.items():

        pdf_path = sources_dir / filename

        print("\n" + "-" * 60)
        print(f"Document: {filename}")

        if not pdf_path.exists():
            print("  STATUS: NOT FOUND")
            print(f"  Expected: {pdf_path}")
            continue

        file_size_mb = pdf_path.stat().st_size / (1024 * 1024)

        print(f"  Title: {title}")
        print(f"  Size: {file_size_mb:.1f} MB")
        print(f"  Document ID: {document_id}")

        # Remove previous version if it exists.
        removed = delete_document(store, document_id)

        if removed:
            print(f"  Removed old chunks: {removed}")
        else:
            print("  No previous chunks found.")

        # Ingest PDF.
        print("  Ingesting PDF...")

        try:
            chunks = store.ingest_pdf(
                str(pdf_path),
                title,
                url,
                document_id,
            )

            total_chunks += chunks

            print(f"  STATUS: SUCCESS")
            print(f"  New chunks: {chunks}")

        except Exception as e:
            print("  STATUS: FAILED")
            print(f"  Error: {e}")

    # -----------------------------------------------------
    # Final status
    # -----------------------------------------------------

    final_count = store.collection.count()

    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)

    print(f"\nChunks ingested during this run: {total_chunks}")
    print(f"Total chunks currently in Chroma: {final_count}")

    print("\nYour persistent RAG database is:")
    print(f"  {project_root / 'data' / 'chroma'}")

    print("\nYou can add more PDFs to:")
    print(f"  {sources_dir}")

    print("\nThen run this same command again.")
    print("=" * 60)


if __name__ == "__main__":
    main()