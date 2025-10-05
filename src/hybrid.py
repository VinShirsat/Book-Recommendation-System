"""Hybrid recommender combining association rules, collaborative, and content-based methods."""
from src.utils import load_books, load_ratings, load_transactions
from src.assoc_rules import mine_fpgrowth, recommend_from_rules
from src.collab import recommend_items_for_user
from src.content import recommend_similar_books


def recommend(user_id=None, book_id=None, method='hybrid', top_n=5):
    books = load_books()
    ratings = load_ratings()
    tx = load_transactions()
    results = []
    if method in ('assoc', 'hybrid') and book_id is not None:
        # find title for book_id
        title = books.loc[books['book_id'] == book_id, 'title'].iloc[0]
        _, rules = mine_fpgrowth(tx, min_support=0.07, min_threshold=0.5)
        assoc = recommend_from_rules(rules, [title], top_n=top_n)
        results.extend([(r[0], 'assoc', r[1], r[2]) for r in assoc])
    if method in ('collab', 'hybrid') and user_id is not None:
        coll = recommend_items_for_user(user_id, ratings, top_n=top_n)
        results.extend(coll)
    if method in ('content', 'hybrid') and book_id is not None:
        content = recommend_similar_books(book_id, books, top_n=top_n)
        results.extend(content)
    return results


def recommend_with_explanations(user_id=None, book_id=None, method='hybrid', top_n=5):
    """Return unified JSON-friendly recommendations with explanations.

    For assoc, uses recommend_with_explanations from assoc_rules; for collab/content returns dicts from those functions.
    """
    books = load_books()
    ratings = load_ratings()
    tx = load_transactions()
    out = []
    if method in ('assoc', 'hybrid') and book_id is not None:
        title = books.loc[books['book_id'] == book_id, 'title'].iloc[0]
        _, rules = mine_fpgrowth(tx, min_support=0.07, min_threshold=0.5)
        from src.assoc_rules import recommend_with_explanations as ar_explain
        out.extend(ar_explain(rules, [title], top_n=top_n))
    if method in ('collab', 'hybrid') and user_id is not None:
        out.extend(recommend_items_for_user(user_id, ratings, top_n=top_n))
    if method in ('content', 'hybrid') and book_id is not None:
        out.extend(recommend_similar_books(book_id, books, top_n=top_n))
    # attach title where missing
    id_to_title = dict(zip(books['book_id'], books['title']))
    for item in out:
        if 'title' not in item:
            if 'book_id' in item and item['book_id'] in id_to_title:
                item['title'] = id_to_title[item['book_id']]
        # attach author and genres where possible
        if 'book_id' in item:
            meta = books[books['book_id'] == item['book_id']]
            if not meta.empty:
                item.setdefault('author', meta['author'].iloc[0])
                item.setdefault('genres', meta['genres'].iloc[0])
    return out
    return out
