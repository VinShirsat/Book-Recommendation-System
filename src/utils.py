import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_books():
    return pd.read_csv(DATA_DIR / "books.csv")

def load_ratings():
    return pd.read_csv(DATA_DIR / "ratings.csv")

def load_transactions():
    return pd.read_csv(DATA_DIR / "transactions.csv")
