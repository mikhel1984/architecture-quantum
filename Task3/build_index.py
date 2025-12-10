import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1024, chunk_overlap=64)

# files to chunks
texts = []
dir_path = os.path.abspath('../Task2/knowledge_base')
for root, directories, files in os.walk(dir_path):
    for filename in files:
        filepath = os.path.join(root, filename)
        # read file
        with open(filepath) as f:
            s = f.read()
            chunks = text_splitter.split_text(s)
            n = 0
            for chunk in chunks:
                texts.append((chunk, str(n), filepath))
                n += len(chunk)

print("chanks:", len(texts))
CHROMA_DATA_PATH = "chroma_data/"
COLLECTION_NAME = "star_wars"

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
  model_name='sentence-transformers/all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_func,
    metadata={"hnsw:space": "cosine"})


chunks = [grp[0] for grp in texts]
collection.add(
    documents=chunks,
    ids=[f'id{i}' for i in range(len(chunks))],
    metadatas=[{"pos": p[1], "file": p[2]} for p in texts]
)
