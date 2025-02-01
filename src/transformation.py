import pandas as pd

def load_and_transform_data(file_path: str) -> pd.DataFrame:
    """
    Loads a Parquet file and applies necessary transformations:
    - Converts timestamps to datetime format.
    - Splits categories into separate entries.
    - Filters out accounts with less than 1000 followers.
    
    :param file_path: Path to the Parquet file.
    :return: Transformed Pandas DataFrame.
    """
    df = pd.read_parquet(file_path)
    
    # Ensure timestamps are in datetime format
    df["date"] = pd.to_datetime(df["date"])
    
    # Filter accounts with more than 1000 followers
    df = df[df["subscriber_count"] > 1000]
    
    # Normalize categories (explode if multiple categories per account)
    df["categories"] = df["categories"].str.split(";")
    df = df.explode("categories")
    
    return df

if __name__ == "__main__":
    file_path = "data/sample_accounts.parquet"
    transformed_df = load_and_transform_data(file_path)
    print(transformed_df.head())

