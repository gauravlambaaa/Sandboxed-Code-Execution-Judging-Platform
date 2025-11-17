
"""Ingest text files from data/docs/ into the Chroma collection."""
import os
from pathlib import Path
from indexer import Indexer

DATA_DIR = Path('data/docs')

def load_docs(data_dir):
    docs = []
    for p in data_dir.glob('**/*'):
        if p.suffix.lower() in ('.txt', '.md'):
            text = p.read_text(encoding='utf-8')
            docs.append({'text': text, 'meta': {'source': str(p)}})
    return docs

if __name__ == '__main__':
    idx = Indexer(collection_name='docs')
    docs = load_docs(DATA_DIR)
    if not docs:
        print('No documents found in data/docs/. Add .txt or .md files and run again.')
    else:
        count = idx.ingest_docs(docs)
        print(f'Ingested {count} chunks into the collection.')
