import pandas as pd


def read_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["is_discounted"] = df["Discount"] > 0
    return df


def create_row_text(row: pd.Series) -> str:
    return (
        f"Order {row['Order ID']} on {row['Order Date']}: "
        f"Customer {row['Customer Name']} from {row['City']}, {row['State']}, {row['Region']} "
        f"ordered {row['Quantity']} '{row['Product Name']}' "
        f"with ship mode {row['Ship Mode']}, generating ${row['Sales']:.2f} in sales and ${row['Profit']:.2f} in profit."
    )


def create_row_texts(df: pd.DataFrame) -> list[str]:
    return [create_row_text(row) for _, row in df.iterrows()]


def create_month_text(row: pd.Series) -> str:
    return (
        f"Monthly orders for {row['Order Date']}: "
        f"Total sales ${row['total_sales']:.2f}, "
        f"Total orders {row['total_orders']}, "
        f"Total profit ${row['total_profit']:.2f}."
    )


def create_month_texts(df: pd.DataFrame) -> list[str]:
    month_rows = (
        df.groupby(df["Order Date"].dt.to_period("M"))
        .agg(
            total_sales=("Sales", "sum"),
            total_orders=("Order ID", "nunique"),
            total_profit=("Profit", "sum"),
        )
        .reset_index()
    )

    return [create_month_text(month_row) for _, month_row in month_rows.iterrows()]


def create_region_text(row: pd.Series) -> str:
    return (
        f"Regional orders for {row['Region']}: "
        f"Total sales ${row['total_sales']:.2f}, "
        f"Total orders {row['total_orders']}, "
        f"Total profit ${row['total_profit']:.2f}."
    )


def create_region_texts(df: pd.DataFrame) -> list[str]:
    region_rows = (
        df.groupby("Region")
        .agg(
            total_sales=("Sales", "sum"),
            total_orders=("Order ID", "nunique"),
            total_profit=("Profit", "sum"),
        )
        .reset_index()
    )

    return [create_region_text(region_row) for _, region_row in region_rows.iterrows()]


def create_category_text(row: pd.Series) -> str:
    return (
        f"Category summary for {row['Category']}: "
        f"Total sales ${row['total_sales']:.2f}, "
        f"Total profit ${row['total_profit']:.2f}."
    )


def create_category_texts(df: pd.DataFrame) -> list[str]:
    category_rows = (
        df.groupby("Category")
        .agg(
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum"),
        )
        .reset_index()
    )

    return [create_category_text(row) for _, row in category_rows.iterrows()]


def create_subcategory_text(row: pd.Series) -> str:
    return (
        f"Sub-Category summary for {row['Sub-Category']}: "
        f"Total sales ${row['total_sales']:.2f}, "
        f"Total profit ${row['total_profit']:.2f}."
    )


def create_subcategory_texts(df: pd.DataFrame) -> list[str]:
    subcategory_rows = (
        df.groupby("Sub-Category")
        .agg(
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum"),
        )
        .reset_index()
    )

    return [create_subcategory_text(row) for _, row in subcategory_rows.iterrows()]


def create_product_text(row: pd.Series) -> str:
    return (
        f"Product summary for {row['product_name']} ({row['Product ID']}): "
        f"Total sales ${row['total_sales']:.2f}, "
        f"Total profit ${row['total_profit']:.2f}, "
        f"Total quantity sold {row['total_quantity']}, "
        f"Total orders {row['total_orders']}, "
        f"Total discounted orders {row['total_discounted_orders']}."
    )


def create_product_texts(df: pd.DataFrame) -> list[str]:
    product_rows = (
        df.groupby("Product ID")
        .agg(
            product_name=("Product Name", "first"),
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum"),
            total_quantity=("Quantity", "sum"),
            total_orders=("Order ID", "nunique"),
            total_discounted_orders=("is_discounted", "sum"),
        )
        .reset_index()
    )

    return [create_product_text(row) for _, row in product_rows.iterrows()]


def create_texts(df: pd.DataFrame) -> list[str]:
    texts = []
    texts += create_row_texts(df)
    texts += create_month_texts(df)
    texts += create_region_texts(df)
    texts += create_category_texts(df)
    texts += create_subcategory_texts(df)
    texts += create_product_texts(df)

    return texts


def chunk_texts(texts: list[str], chunk_size: int = 500) -> list[str]:
    chunked_texts = []
    for text in texts:
        if len(text) <= chunk_size:
            chunked_texts.append(text)
        else:
            current = []
            current_length = 0
            for word in text.split():
                if current_length + len(word) + 1 > chunk_size:
                    chunked_texts.append(" ".join(current))
                current.append(word)
                current_length += len(word) + 1
            if current:
                chunked_texts.append(" ".join(current))

    return chunked_texts
