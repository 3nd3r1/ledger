import logging

from preparation import create_texts, read_data


def main():
    logging.basicConfig(
        level=logging.DEBUG,
    )

    df = read_data("data/superstore.csv")
    texts = create_texts(df)

    print(texts)


if __name__ == "__main__":
    main()
