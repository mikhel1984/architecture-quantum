import os
import tiktoken

def chunk_by_tokens(text: str, max_tokens: int = 128, overlap: int = 32, enc=None):
    enc = enc or tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk = enc.decode(tokens[start:end])
        yield chunk, start
        start = end - overlap  # шаг назад для overlap


texts = {}
dir_path = os.path.abspath('../Task2/knowledge_base')

for root, directories, files in os.walk(dir_path):
    for filename in files:
        filepath = os.path.join(root, filename)
        # read file
        with open(filepath) as f:
            s = f.read()
            lst = []
            for ch, pos in chunk_by_tokens(s, 600, 60):
                lst.append((ch, pos))
            texts[filepath] = lst
            print(len(lst))

