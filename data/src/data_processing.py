# src/data_processing.py
from pathlib import Path
from typing import Union
import pandas as pd

def load_metadata(path: Union[str, Path]) -> pd.DataFrame:
    """Load CSV with basic error handling and try to parse publish_time."""
    path = Path(path)
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV: {e}")

    # try parse publish_time to datetime if present
    if "publish_time" in df.columns:
        df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    return df

def clean_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Drop completely empty rows, fill common NaNs, add derived columns."""
    df = df.copy()
    df.dropna(how="all", inplace=True)

    # Fill missing journal/source/authors with 'Unknown'
    for col in ["journal", "source", "authors"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Add publish_year column if publish_time exists
    if "publish_time" in df.columns:
        df["publish_year"] = df["publish_time"].dt.year
    else:
        df["publish_year"] = pd.NA

    # Add abstract_word_count
    if "abstract" in df.columns:
        df["abstract"] = df["abstract"].fillna("")
        df["abstract_word_count"] = df["abstract"].str.split().apply(len)
    else:
        df["abstract_word_count"] = 0

    return df
