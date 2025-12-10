import chromadb
import sys

CHROMA_DATA_PATH = "chroma_data/"
COLLECTION_NAME = "star_wars"

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

if len(sys.argv) > 1:
  matched_docs = collection.query(query_texts=[sys.argv[1]], n_results=1)

  print(matched_docs)


