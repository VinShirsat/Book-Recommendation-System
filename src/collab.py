"""Item-based collaborative filtering recommender.

- build_user_item_matrix(ratings_df)
- item_similarity_matrix(ratings_df)
- recommend_items_for_user(user_id, ratings_df, top_n=5)
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.utils import load_books


def build_user_item_matrix(ratings_df):
    return ratings_df.pivot_table(index='user_id', columns='book_id', values='rating').fillna(0)


def item_similarity_matrix(ratings_df):
    ui = build_user_item_matrix(ratings_df)
    # columns are book_id
    sim = cosine_similarity(ui.T)
    sim_df = pd.DataFrame(sim, index=ui.columns, columns=ui.columns)
    return sim_df


def recommend_items_for_user(user_id, ratings_df, top_n=5):
    ui = build_user_item_matrix(ratings_df)
    sim = item_similarity_matrix(ratings_df)
    if user_id not in ui.index:
        return []
    user_ratings = ui.loc[user_id]
    # score = sum(similarity * rating) / sum(abs(sim))
    scores = sim.dot(user_ratings) / (sim.abs().sum(axis=1) + 1e-8)
    # remove already rated
    rated = user_ratings[user_ratings > 0].index
    scores = scores.drop(index=rated)
    top = scores.sort_values(ascending=False).head(top_n)
    # provide simple explanation: top contributing items
    results = []
    books = load_books()
    id_to_title = dict(zip(books['book_id'], books['title']))
    for item_id, score in top.items():
        # find top contributing items (similar items the user rated)
        contrib = sim.loc[item_id].multiply(user_ratings).nlargest(3)
        contrib = [(int(idx), float(val)) for idx, val in contrib.items() if val > 0]
        # map ids to titles for explanation
        contrib_titles = [(id_to_title.get(int(idx), f'Book {idx}'), val) for idx, val in contrib]
        # enrich with author and genres if available
        book_title = id_to_title.get(int(item_id), f'Book {item_id}')
        # load authors/genres map
        books_df = load_books()
        meta = books_df[books_df['book_id'] == int(item_id)]
        if not meta.empty:
            author = meta['author'].iloc[0]
            genres = meta['genres'].iloc[0]
        else:
            author = None
            genres = None
        results.append({'book_id': int(item_id), 'title': book_title, 'author': author, 'genres': genres, 'method': 'collab', 'score': float(score), 'contrib': contrib_titles})
    return results
