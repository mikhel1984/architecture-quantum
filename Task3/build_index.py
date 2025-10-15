import os
import tiktoken
import chromadb
from chromadb.utils import embedding_functions

def chunk_by_tokens(text: str, max_tokens: int = 128, overlap: int = 32, enc=None):
    enc = enc or tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk = enc.decode(tokens[start:end])
        yield chunk, start
        start = end - overlap  # шаг назад для overlap


# files to chunks
texts = []
dir_path = os.path.abspath('../Task2/knowledge_base')
for root, directories, files in os.walk(dir_path):
    for filename in files:
        filepath = os.path.join(root, filename)
        # read file
        with open(filepath) as f:
            s = f.read()
            lst = []
            for ch, pos in chunk_by_tokens(s, 600, 60):
                lst.append((ch, pos, filepath))
            texts += lst


CHROMA_DATA_PATH = "chroma_data/"
EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "star_wars"

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL)
collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_func,
    metadata={"hnsw:space": "cosine"})


chunks = [grp[0] for grp in texts]
collection.add(
    documents=chunks,
    ids=[f'id{i}' for i in range(len(chunks))],
    metadatas=[{"pos": p[1], "file": p[2]} for p in chunks]
)
