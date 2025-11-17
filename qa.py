
"""Interactive QA loop that answers questions using retrieved context and
invokes auto-reindexing when answers appear low-quality.

This is a simple developer demo. In production, reindexing would be incremental
and update only affected items, not delete the entire collection.
"""
import os
from dotenv import load_dotenv
from langchain import OpenAI
from retriever import Retriever
from indexer import Indexer
from utils import is_low_quality_answer, rechunk_text

load_dotenv()

llm = OpenAI(temperature=0)
retriever = Retriever()
indexer = Indexer()

def ask_loop():
    print('Interactive QA — type `exit` to quit')
    while True:
        q = input('\nQuestion: ').strip()
        if q.lower() in ('exit', 'quit'):
            break
        res = retriever.retrieve(q, k=4)
        docs = res.get('documents', [[]])[0]
        metadatas = res.get('metadatas', [[]])[0]
        print('\n--- Retrieved snippets ---')
        for i, d in enumerate(docs):
            print(f'[{i}]', (d[:300] + '...') if len(d) > 300 else d)
        prompt = f"Use the context below to answer the question concisely. If unknown, say 'I don't know'.\n\nCONTEXT:\n{'\n\n'.join(docs)}\n\nQ: {q}\nA:"
        ans = llm(prompt)
        print('\nAnswer:\n', ans)
        if is_low_quality_answer(str(ans)):
            print('\n[Auto-Reindex] Detected low-quality answer. Rechunking top parent docs and reindexing...')
            parent_ids = set()
            for md in metadatas:
                pid = md.get('parent_id')
                if pid is not None:
                    parent_ids.add(pid)
            to_reingest = []
            # Try to reconstruct source texts from metadata 'source' if available
            for pid in parent_ids:
                sources = [md.get('source') for md in metadatas if md.get('parent_id') == pid and md.get('source')]
                if not sources:
                    continue
                src = sources[0]
                try:
                    text = open(src, 'r', encoding='utf-8').read()
                except Exception:
                    continue
                chunks = rechunk_text(text, chunk_size=500, overlap=50)
                to_reingest.append({'text': '\n\n'.join(chunks), 'meta': {'source': src}})
            if to_reingest:
                print('Rebuilding collection (dev-mode: full rebuild). This may take a moment.')
                indexer.delete_collection()
                indexer = Indexer()
                # Read all docs from data/docs to preserve dataset; fallback to reingest to_reingest only
                base = 'data/docs'
                all_docs = []
                import pathlib
                for p in pathlib.Path(base).glob('**/*'):
                    if p.suffix.lower() in ('.txt', '.md'):
                        all_docs.append({'text': p.read_text(encoding='utf-8'), 'meta': {'source': str(p)}})
                if all_docs:
                    indexer.ingest_docs(all_docs)
                else:
                    indexer.ingest_docs(to_reingest)
                print('Reindex done. Try the question again.')
            else:
                print('Could not locate source files to reindex. Consider re-ingesting with full documents in data/docs/')

if __name__ == '__main__':
    ask_loop()
