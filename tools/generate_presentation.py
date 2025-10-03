from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

OUT = 'presentation.pdf'

slides = [
    {"title": "Book Recommendation System — Overview", "bullets": [
        "Three recommenders: Association Rules (FP-Growth), Item-based Collaborative, Content-based (TF-IDF)",
        "Hybrid endpoint combines outputs and provides explanations", 
        "Flask UI with AJAX, visualization panels: top rules, clusters, evaluation"
    ]},
    {"title": "Data & Inputs", "bullets": [
        "books.csv: book_id, title, author, description, genres",
        "ratings.csv: user_id, book_id, rating (used by collaborative filtering)",
        "transactions.csv: transaction_id, items (used by association rule mining)"
    ]},
    {"title": "Association Rules (FP-Growth)", "bullets": [
        "Convert transactions to one-hot matrix with TransactionEncoder (mlxtend)",
        "Run fpgrowth to get frequent itemsets (support)",
        "Generate rules with association_rules (confidence, lift)",
        "Use rules to suggest consequents given antecedents (market-basket)",
    ]},
    {"title": "Item-based Collaborative Filtering", "bullets": [
        "Build user-item matrix from ratings (users x books)",
        "Compute item-item similarity using cosine similarity on item vectors",
        "Score unknown items for a user with weighted sum of similarity*rating",
        "Provide explanations: top contributing items that influenced score"
    ]},
    {"title": "Content-based (TF-IDF)", "bullets": [
        "TF-IDF vectorizer on book descriptions (stop words removed)",
        "Cosine similarity between TF-IDF vectors to find most similar books",
        "Useful for cold-start items with descriptive metadata"
    ]},
    {"title": "Comparison & When to Use Which", "bullets": [
        "Association: good for bundle/cross-sell when transaction data abundant",
        "Collaborative: personalized, needs sufficient user ratings; susceptible to cold-start",
        "Content: works with item metadata; good for new items but not personalized",
        "Hybrid: combines strengths — use ensemble or weighted combination"
    ]},
    {"title": "Evaluation Metrics", "bullets": [
        "Precision@k, Recall@k, MAP, NDCG — use time-aware split for realism",
        "Quick demo uses a random train/test split and precision@5 (demo only)"
    ]},
    {"title": "Demo Flow & Talking Points", "bullets": [
        "Start UI -> demonstrate Association Rules, Collaborative, Content-based, Hybrid",
        "Show top rules panel, clusters, and evaluation metric",
        "Explain mapping to syllabus units (Unit V => FP-Growth, Unit IV => clustering, Unit VI => visualization)"
    ]},
]


def draw_slide(c, slide):
    c.setFont('Helvetica-Bold', 24)
    c.drawCentredString(11*inch/2, 7*inch, slide['title'])
    c.setFont('Helvetica', 14)
    y = 6*inch
    for b in slide['bullets']:
        c.drawString(1*inch, y, u'• ' + b)
        y -= 0.6*inch


if __name__ == '__main__':
    c = canvas.Canvas(OUT, pagesize=landscape(A4))
    for s in slides:
        draw_slide(c, s)
        c.showPage()
    c.save()
    print('Wrote', OUT)
