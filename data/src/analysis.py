# src/analysis.py
from typing import Tuple, List
import pandas as pd
from collections import Counter
import re

def basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return describe() for numeric columns."""
    return df.describe(include="number").T

def publications_per_year(df: pd.DataFrame) -> pd.Series:
    """Return counts of papers per year (sorted)."""
    if "publish_year" not in df.columns:
        return pd.Series(dtype=int)
    return df["publish_year"].dropna().astype(int).value_counts().sort_index()

def top_journals(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Return top n journals by count."""
    if "journal" not in df.columns:
        return pd.Series(dtype=int)
    return df["journal"].fillna("Unknown").value_counts().head(n)

def top_title_words(df: pd.DataFrame, n: int = 20, stopwords: List[str] = None) -> List[Tuple[str, int]]:
    """Return most frequent words in titles (simple cleaning)."""
    stopwords = set(stopwords or [])
    titles = df.get("title", pd.Series(dtype=str)).fillna("").str.lower()
    words = []
    for t in titles:
        tokens = re.findall(r"\b[a-zA-Z]{2,}\b", t)
        words.extend([w for w in tokens if w not in stopwords])
    counts = Counter(words).most_common(n)
    return counts