from flask import Flask, render_template, request, jsonify
from src.hybrid import recommend_with_explanations
from src.utils import load_books

import csv
from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
BOOKS_CSV = DATA_DIR / 'books.csv'

app = Flask(__name__)

books = load_books()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', books=books.to_dict('records'))


@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    data = request.json or {}
    method = data.get('method', 'hybrid')
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    top_n = int(data.get('top_n', 5))
    user_id = int(user_id) if user_id else None
    book_id = int(book_id) if book_id else None
    recs = recommend_with_explanations(user_id=user_id, book_id=book_id, method=method, top_n=top_n)
    return jsonify({'recs': recs})


@app.route('/api/top_rules', methods=['GET'])
def api_top_rules():
    from src.assoc_rules import mine_fpgrowth, top_k_rules
    tx = load_books()  # placeholder to avoid circular imports; we'll load transactions inside
    from src.utils import load_transactions
    tx = load_transactions()
    _, rules = mine_fpgrowth(tx, min_support=0.1, min_threshold=0.5)
    rules_out = top_k_rules(rules, k=10)
    return jsonify({'rules': rules_out})


@app.route('/api/eval', methods=['GET'])
def api_eval():
    from src.utils import load_ratings
    from src.eval import quick_eval
    ratings = load_ratings()
    res = quick_eval(ratings, k=5)
    return jsonify(res)


@app.route('/api/clusters', methods=['GET'])
def api_clusters():
    from src.utils import load_ratings
    from src.visualize import cluster_users
    ratings = load_ratings()
    res = cluster_users(ratings, n_clusters=3)
    return jsonify(res)


@app.route('/api/books', methods=['GET'])
def api_books():
    books = load_books()
    return jsonify({'books': books.to_dict('records')})


@app.route('/api/add_book', methods=['POST'])
def api_add_book():
    data = request.json or {}
    title = data.get('title')
    author = data.get('author', '')
    description = data.get('description', '')
    genres = data.get('genres', '')
    if not title:
        return jsonify({'error': 'title required'}), 400
    # find next id
    books = load_books()
    next_id = int(books['book_id'].max()) + 1 if not books.empty else 1
    # append to CSV
    with open(BOOKS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([next_id, title, author, description, genres])
    return jsonify({'ok': True, 'book': {'book_id': next_id, 'title': title, 'author': author, 'genres': genres}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
