# tests/test_data.py
from src.data_processing import load_metadata, clean_metadata
from pathlib import Path

SAMPLE = Path("data/sample_metadata.csv")

def test_load_sample_exists():
    df = load_metadata(SAMPLE)
    assert df.shape[0] > 0

def test_clean_has_columns():
    df = load_metadata(SAMPLE)
    df2 = clean_metadata(df)
    assert "abstract_word_count" in df2.columns
    # publish_year may be NaN for missing dates but column should exist
    assert "publish_year" in df2.columns