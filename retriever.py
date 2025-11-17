
from indexer import Indexer

class Retriever:
    def __init__(self, collection_name='docs'):
        self.indexer = Indexer(collection_name=collection_name)

    def retrieve(self, query, k=4):
        return self.indexer.query(query, k=k)
