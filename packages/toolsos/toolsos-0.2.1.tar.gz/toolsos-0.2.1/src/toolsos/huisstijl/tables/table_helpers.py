import pandas as pd


def remove_underscores_from_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.replace("_", " ")
    return df
