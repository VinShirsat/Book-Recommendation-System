Demo script — Book Recommendation System

Goal: Present a short demo to your teacher showing three recommendation approaches (Association rules, Collaborative, Content-based), a hybrid view, and supportive visualizations (top rules, clusters, quick evaluation).

Before the demo
- From project root in PowerShell, activate venv:
  .venv\Scripts\Activate.ps1
- Start the demo (this opens your browser to the UI):
  .\start_demo.ps1

If you prefer to run in the foreground (recommended to show logs), run:
  .venv\Scripts\python.exe -m src.webapp

Step-by-step demo (approx. 6-10 minutes)
1. Quick intro (30s)
   - One slide or verbal: Purpose — recommend books using syllabus algorithms: FP-Growth (association rules), item-based collaborative filtering, and TF-IDF content-based similarity. Show the project structure briefly.

2. Association Rules (1-2 min)
   - UI: Set Method -> Association Rules, Book ID -> 6 ("Recommender Systems Handbook"), Top N -> 5, click "Get Recommendations".
   - Expected output: Recommendations list with rules like "{Recommender Systems Handbook} => {Hands-On Machine Learning}" (example depends on mined rules). Click one item and the Explanation panel shows the rule text, support, confidence and lift.
   - Talking points tied to syllabus: Unit V (Association Rule Mining). Explain support/confidence/lift and FP-Growth avoiding candidate generation (compare to Apriori briefly).

3. Collaborative Filtering (1-2 min)
   - UI: Set Method -> Collaborative, User ID -> 1, Top N -> 5, click "Get Recommendations".
   - Expected output: Personalized suggestions (title, author, genres). Click one item and the Explanation shows the score and top contributing items (the books that caused the recommendation). Explain neighborhood/item-similarity and cosine similarity.
   - Syllabus tie: Unit III/IV (classification/cluster ideas, neighborhood methods).

4. Content-based (1-2 min)
   - UI: Set Method -> Content-based, Book ID -> 2 ("Hands-On Machine Learning"), Top N -> 5, click "Get Recommendations".
   - Expected output: Books with similar textual descriptions; Explanation shows similarity score and metadata.
   - Syllabus tie: Unit VI (feature extraction and data visualization). Mention TF-IDF and cosine similarity on text features.

5. Hybrid and extras (1-2 min)
   - UI: Method -> Hybrid, choose User ID and Book ID and compare outputs: Hybrid combines assoc/collab/content outputs.
   - Click "Load Top Rules" panel to show the top association rules mined (useful for explaining FP-Growth outcome).
   - Click "Load Clusters" to show simple cluster counts. Click "Run Quick Eval" to show a demo metric (precision@5) computed on a small holdout.

6. Q&A and code walkthrough (remaining time)
   - Show the relevant files: `src/assoc_rules.py` (FP-Growth mining, `association_rules` usage), `src/collab.py` (user-item matrix and cosine similarity), `src/content.py` (TF-IDF, linear_kernel), `src/hybrid.py` (combination), and `src/webapp.py` (UI endpoints).
   - Explain data shapes: `books.csv` (book_id,title,author,description,genres), `ratings.csv` (user_id,book_id,rating), `transactions.csv` (transaction_id,items). Explain how transactions are converted into lists for FP-Growth.

Notes for the demo
- Book ID mapping (quick reference):
  1 — Introduction to Data Science (Joel Grus)
  2 — Hands-On Machine Learning (Aurélien Géron)
  3 — Deep Learning (Goodfellow Deep)
  4 — Practical Statistics for Data Scientists (Peter Bruce)
  5 — Pattern Recognition and ML (Christopher Bishop)
  6 — Recommender Systems Handbook (Francesco Ricci)
  7 — Python for Data Analysis (Wes McKinney)
  8 — Data Visualization with Python (Alberto Cairo)
  9 — Introduction to Algorithms (CLRS)
  10 — Marketing Analytics (Practical Marketing)

- User ID usage: User IDs correspond to rows in `ratings.csv` that hold user ratings for books. Use User ID to generate personalized recommendations with the collaborative recommender. Example user IDs in the sample data: 1..10.

Troubleshooting
- If the page shows an error, check the terminal for Flask logs and restart the app.
- If association rules return no rules, try lowering the minimum support / confidence in code (in `src/assoc_rules.py` or `src/hybrid.py`).

Closing (30s)
- Summarize which syllabus units each method matches: Association Rules (Unit V), Collaborative (Unit III/IV), TF-IDF / Visualization (Unit VI). Offer to show code snippets or evaluations after questions.

Good luck with your demo — tell me if you want this as a printable PDF or a short slide deck (3 slides) to accompany your presentation.
