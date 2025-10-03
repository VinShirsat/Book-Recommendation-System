import pandas as pd
from sklearn.cluster import KMeans
from src.collab import build_user_item_matrix


def cluster_users(ratings_df, n_clusters=3):
    ui = build_user_item_matrix(ratings_df)
    if ui.shape[0] < n_clusters:
        n_clusters = max(1, ui.shape[0])
    km = KMeans(n_clusters=n_clusters, random_state=42)
    labels = km.fit_predict(ui)
    df = pd.DataFrame({'user_id': ui.index, 'cluster': labels})
    counts = df['cluster'].value_counts().sort_index().to_dict()
    return {'labels': df.to_dict('records'), 'counts': counts}
