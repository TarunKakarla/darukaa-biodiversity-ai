from app.rag.store import RAGStore
store = RAGStore()
for item in store.retrieve("semi-arid monoculture wheat low soil organic carbon agroforestry intercropping", 5):
    print("\nSOURCE:", item["metadata"]["source_title"])
    print("URL:", item["metadata"]["source_url"])
    print(item["text"][:700])
