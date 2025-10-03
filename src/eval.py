import pandas as pd
from sklearn.model_selection import train_test_split
from src.collab import recommend_items_for_user


def precision_at_k(recommended_ids, relevant_ids, k):
    recommended_topk = [r for r in recommended_ids[:k]]
    if not recommended_topk:
        return 0.0
    relevant_set = set(relevant_ids)
    hits = sum(1 for r in recommended_topk if r in relevant_set)
    return hits / k


def quick_eval(ratings_df, k=5, test_size=0.2, random_state=42):
    # split by user interactions
    train, test = train_test_split(ratings_df, test_size=test_size, random_state=random_state)
    users = test['user_id'].unique()
    precisions = []
    for u in users:
        # items in test for user
        relevant = test[test['user_id'] == u]['book_id'].tolist()
        if not relevant:
            continue
        recs = recommend_items_for_user(u, train, top_n=k)
        # recs is list of dicts
        rec_ids = [r['book_id'] for r in recs]
        precisions.append(precision_at_k(rec_ids, relevant, k))
    if not precisions:
        return {'precision_at_k': None}
    return {'precision_at_k': float(sum(precisions) / len(precisions))}
