"""Content-based recommender using TF-IDF on book descriptions.

- build_tfidf_matrix(books_df)
- recommend_similar_books(book_id, books_df, top_n=5)
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def build_tfidf_matrix(books_df):
    desc = books_df['description'].fillna('')
    tf = TfidfVectorizer(stop_words='english')
    tfidf = tf.fit_transform(desc)
    return tfidf, tf


def recommend_similar_books(book_id, books_df, top_n=5):
    tfidf, tf = build_tfidf_matrix(books_df)
    idx = books_df.index[books_df['book_id'] == book_id].tolist()
    if not idx:
        return []
    idx = idx[0]
    cosine_similarities = linear_kernel(tfidf[idx:idx+1], tfidf).flatten()
    # remove itself
    cosine_similarities[idx] = -1
    sim_idx = cosine_similarities.argsort()[::-1][:top_n]
    results = []
    for i in sim_idx:
        bid = int(books_df.iloc[i]['book_id'])
        meta = books_df.iloc[i]
        results.append({'book_id': bid, 'title': meta['title'], 'author': meta.get('author', None), 'genres': meta.get('genres', None), 'method': 'content', 'score': float(cosine_similarities[i]), 'similar_to': int(books_df.iloc[idx]['book_id'])})
    return results
