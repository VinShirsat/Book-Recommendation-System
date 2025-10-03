"""Simple CLI to run recommendations."""
import argparse
import sys
from pathlib import Path

# Make imports work whether run as `python src/run.py` or as a module
try:
    # when run as module (python -m src.run)
    from src.hybrid import recommend
except Exception:
    # fallback for script execution
    try:
        from hybrid import recommend
    except Exception:
        print("Failed to import recommender modules. Make sure you run this from project root or install package dependencies.")
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', choices=['assoc','collab','content','hybrid'], default='hybrid')
    parser.add_argument('--user_id', type=int, default=None)
    parser.add_argument('--book_id', type=int, default=None)
    parser.add_argument('--top_n', type=int, default=5)
    args = parser.parse_args()
    recs = recommend(user_id=args.user_id, book_id=args.book_id, method=args.method, top_n=args.top_n)
    print('Recommendations:')
    for r in recs:
        print(r)

if __name__ == '__main__':
    main()
