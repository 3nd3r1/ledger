import logging

from chromadb.utils import embedding_functions

import chromadb


logger = logging.getLogger(__name__)


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

    def clear(self):
        self._client.delete_collection("superstore")
        self._collection = self._client.get_or_create_collection(
            name="superstore",
            embedding_function=self._embedding_function,  # type: ignore
        )
        logger.info("Cleared the vector store.")

    def add_chunks(self, chunks: list[tuple[str, dict]]):
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            ids = [f"doc_{i + j}" for j in range(len(batch))]  # i is the batch offset
            self._collection.add(
                ids=ids,
                documents=[text for text, _ in batch],
                metadatas=[meta for _, meta in batch],
            )
        logger.info(f"Added {len(chunks)} chunks to the vector store.")

    def search(self, query: str, n_results: int = 10, where: dict | None = None) -> list[dict]:
        logger.debug(f"Searching for '{query}' (top {n_results}){f', filter: {where}' if where else ''}")
        results = self._collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
        )

        docs = []
        for i in range(len(results["ids"][0])):
            docs.append(
                {
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],  # type: ignore
                    "metadata": results["metadatas"][0][i],  # type: ignore
                    "distance": results["distances"][0][i],  # type: ignore
                }
            )

        return docs
