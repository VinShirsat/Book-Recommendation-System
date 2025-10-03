Book Recommendation System

This is a minimal Python project demonstrating three recommendation strategies aligned with the syllabus:
- Association rules (Apriori / FP-Growth) — maps to Unit V Association Rule mining (FP-Growth, Apriori)
- Item-based Collaborative Filtering — maps to Unit III Classification/Regression & Unit IV Clustering (neighborhoods)
- Content-based (TF-IDF on descriptions) — maps to Unit VI Data Visualization / feature extraction

Contents:
- src/: source code for recommenders and runner
- data/: small sample datasets (books, ratings, transactions)
- requirements.txt: Python dependencies

How to run (after installing requirements):
1. python -m pip install -r requirements.txt
2. python src/run.py --method assoc --book_id 1

Project layout and mapping to syllabus are documented in the README and in `src/` docstrings.
