import logging

from chromadb.utils import embedding_functions

import chromadb


class VectorStore:
    def __init__(self):
        self._embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )
        self._client = chromadb.PersistentClient(path="./chromadb")
        self._collection = self._client.get_or_create_collection(
            name="superstore",
            embedding_function=self._embedding_function,  # type: ignore
        )

    def add_chunks(self, chunks: list[str]):
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i : i + batch_size]
            ids = [f"doc_{i + j}" for j in range(i, i + len(batch_chunks))]
            self._collection.add(
                ids=ids,
                documents=batch_chunks,
            )
        logging.info(f"Added {len(chunks)} chunks to the vector store.")
