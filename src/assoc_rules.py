"""Association-rule recommender using FP-Growth / Apriori (mlxtend)

Implements:
- build_itemsets(transactions_df)
- mine_fpgrowth(transactions_df, min_support=0.1)
- recommend_from_rules(rules_df, seed_items, top_n=5)

This maps to Unit V Association Rule mining in the syllabus (FP-Growth, Apriori).
"""
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
import pandas as pd


def build_itemsets(transactions_df):
    # transactions_df has a column 'items' with comma separated book titles
    tx = transactions_df['items'].apply(lambda s: [i.strip() for i in s.split(',')])
    return tx.tolist()


def mine_fpgrowth(transactions_df, min_support=0.07, min_threshold=0.5):
    # Lowered min_support to 0.07 (about 2 transactions in 30) and min_threshold to 0.5 for more rules
    tx = build_itemsets(transactions_df)
    te = TransactionEncoder()
    te_ary = te.fit(tx).transform(tx)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    freq = fpgrowth(df, min_support=min_support, use_colnames=True)
    rules = association_rules(freq, metric="confidence", min_threshold=min_threshold)
    return freq, rules


def recommend_from_rules(rules_df, seed_items, top_n=5):
    """Given seed_items (list of item names), return top_n recommended consequents sorted by lift then confidence."""
    # filter rules where antecedents are subset of seed_items
    seed_set = set(seed_items)
    # rules_df antecedents and consequents are frozensets
    matches = []
    for _, row in rules_df.iterrows():
        if set(row['antecedents']).issubset(seed_set) and not set(row['consequents']).issubset(seed_set):
            matches.append((tuple(row['consequents']), row['lift'], row['confidence']))
    if not matches:
        return []
    # sort by lift then confidence
    matches.sort(key=lambda x: ( -x[1], -x[2]))
    seen = set()
    recs = []
    for consequents, lift, conf in matches:
        for c in consequents:
            if c not in seen:
                recs.append((c, lift, conf))
                seen.add(c)
            if len(recs) >= top_n:
                break
        if len(recs) >= top_n:
            break
    return recs


def recommend_with_explanations(rules_df, seed_items, top_n=5):
    """Return structured recommendations with explanations for the given seed_items.

    Each recommendation is a dict: {"title", "method": "assoc", "score": lift, "confidence", "support", "rule"}
    """
    seed_set = set(seed_items)
    matches = []
    for _, row in rules_df.iterrows():
        if set(row['antecedents']).issubset(seed_set) and not set(row['consequents']).issubset(seed_set):
            consequents = list(row['consequents'])
            matches.append({'consequents': consequents, 'lift': float(row.get('lift', 0)), 'confidence': float(row.get('confidence', 0)), 'support': float(row.get('support', 0)), 'antecedents': list(row['antecedents'])})
    if not matches:
        return []
    # sort by lift, confidence
    matches.sort(key=lambda x: (-x['lift'], -x['confidence']))
    recs = []
    seen = set()
    for m in matches:
        for c in m['consequents']:
            if c in seen:
                continue
            seen.add(c)
            rule_text = f"{{{', '.join(m['antecedents'])}}} => {{{c}}}"
            # try to map title to metadata if books available
            rec_item = {'title': c, 'method': 'assoc', 'score': m['lift'], 'confidence': m['confidence'], 'support': m['support'], 'rule': rule_text}
            recs.append(rec_item)
            if len(recs) >= top_n:
                break
        if len(recs) >= top_n:
            break
    return recs


def top_k_rules(rules_df, k=10):
    """Return top-k rules sorted by lift for display/logging."""
    if rules_df is None or rules_df.empty:
        return []
    top = rules_df.sort_values(by='lift', ascending=False).head(k)
    out = []
    for _, row in top.iterrows():
        out.append({'antecedents': list(row['antecedents']), 'consequents': list(row['consequents']), 'support': float(row.get('support', 0)), 'confidence': float(row.get('confidence', 0)), 'lift': float(row.get('lift', 0))})
    return out
