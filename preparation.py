import pandas as pd


def read_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df


def create_row_text(row: pd.Series) -> str:
    return (
        f"Order {row['Order ID']} on {row['Order Date']}: "
        f"Customer {row['Customer Name']} from {row['City']}, {row['State']}, {row['Region']} "
        f"ordered {row['Quantity']} '{row['Product Name']}' "
        f"with ship mode {row['Ship Mode']}, generating {row['Sales']} in sales and {row['Profit']} in profit."
    )


def create_row_texts(df: pd.DataFrame) -> list[str]:
    return [create_row_text(row) for _, row in df.iterrows()]


def create_month_text(row: pd.Series) -> str:
    return (
        f"Monthly orders for {row['Order Date']}: "
        f"Total sales {row['total_sales']}, "
        f"Total orders {row['total_orders']}, "
        f"Total profit {row['total_profit']}."
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
        f"Total sales {row['total_sales']}, "
        f"Total orders {row['total_orders']}, "
        f"Total profit {row['total_profit']}."
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


def create_texts(df: pd.DataFrame) -> list[str]:
    texts = []
    texts += create_row_texts(df)
    texts += create_month_texts(df)
    texts += create_region_texts(df)

    return texts
