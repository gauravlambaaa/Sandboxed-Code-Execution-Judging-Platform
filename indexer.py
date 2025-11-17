
"""Indexing module using Chroma and OpenAI embeddings via LangChain."""
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import chromadb
from chromadb.config import Settings

CHROMA_SETTINGS = Settings()

class Indexer:
    def __init__(self, collection_name='docs'):
        self.client = chromadb.Client(CHROMA_SETTINGS)
        # create or get collection
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.emb = OpenAIEmbeddings()

    def ingest_docs(self, docs: list, ids_prefix='doc'):
        texts = []
        metadatas = []
        ids = []
        for i, d in enumerate(docs):
            chunks = self.splitter.split_text(d['text'])
            for j, c in enumerate(chunks):
                texts.append(c)
                md = dict(d.get('meta', {}))
                md['parent_id'] = i
                metadatas.append(md)
                ids.append(f"{ids_prefix}-{i}-{j}")
        # add to chroma in batches
        batch = 500
        for start in range(0, len(texts), batch):
            end = start + batch
            self.collection.add(documents=texts[start:end], metadatas=metadatas[start:end], ids=ids[start:end])
        return len(ids)

    def query(self, q, k=4):
        res = self.collection.query(query_texts=[q], n_results=k, include=['documents','metadatas','ids'])
        return res

    def delete_collection(self):
        self.collection.delete()
