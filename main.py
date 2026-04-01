import logging

from preparation import chunk_texts, create_texts, read_data
from vector_store import VectorStore


def main():
    logging.basicConfig(
        level=logging.DEBUG,
    )

    df = read_data("data/superstore.csv")

    texts = create_texts(df)

    chunks = chunk_texts(texts)

    store = VectorStore()
    store.add_chunks(chunks)


if __name__ == "__main__":
    main()
