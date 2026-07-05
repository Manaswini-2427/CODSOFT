"""
recommender.py
A simple content-based movie recommendation system.

No external dataset needed -- a small sample catalog is included so you can
run this immediately.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


# 1. Sample data 
movies = pd.DataFrame([
    {"movie_id": 1, "title": "The Matrix",         "genre": "Action Sci-Fi",     "description": "A hacker discovers reality is a simulation and joins a rebellion against machines."},
    {"movie_id": 2, "title": "Inception",           "genre": "Action Sci-Fi",     "description": "A thief who steals secrets through dream-sharing technology takes on a mind-bending heist."},
    {"movie_id": 3, "title": "Interstellar",        "genre": "Sci-Fi Drama",      "description": "Explorers travel through a wormhole in search of a new home for humanity."},
    {"movie_id": 4, "title": "The Notebook",        "genre": "Romance Drama",     "description": "A poor young man falls in love with a rich young woman in a story spanning decades."},
    {"movie_id": 5, "title": "Titanic",             "genre": "Romance Drama",     "description": "A love story unfolds aboard the ill-fated ship on its maiden voyage."},
    {"movie_id": 6, "title": "John Wick",           "genre": "Action Thriller",   "description": "A retired hitman seeks vengeance against the gangsters who took everything from him."},
    {"movie_id": 7, "title": "The Conjuring",       "genre": "Horror Thriller",   "description": "Paranormal investigators help a family terrorized by a dark presence in their farmhouse."},
    {"movie_id": 8, "title": "Get Out",             "genre": "Horror Thriller",   "description": "A young man uncovers a disturbing secret when he visits his girlfriend's family estate."},
    {"movie_id": 9, "title": "La La Land",          "genre": "Romance Musical",   "description": "An aspiring actress and a jazz musician fall in love while pursuing their dreams."},
    {"movie_id": 10, "title": "Mad Max: Fury Road", "genre": "Action Adventure",  "description": "A woman rebels against a tyrannical ruler in a post-apocalyptic wasteland."},
])

user_ratings = {
    "alice": [1, 2],      
    "bob":   [4, 5],      
    "carol": [7, 8],      
}


# 2. Build the content-based recommender

class ContentBasedRecommender:
    def __init__(self, items: pd.DataFrame, id_col: str, text_cols: list):
        """
        Args:
            items: DataFrame of items (movies/books/products).
            id_col: name of the unique identifier column.
            text_cols: columns to combine into a single text blob per item
                (e.g. genre + description) used to measure similarity.
        """
        self.items = items.reset_index(drop=True)
        self.id_col = id_col
        self.items["_combined_text"] = self.items[text_cols].agg(" ".join, axis=1)

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.items["_combined_text"])

        # Precompute similarity between every pair of items.
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)

        self._id_to_index = {
            item_id: idx for idx, item_id in enumerate(self.items[self.id_col])
        }

    def similar_items(self, item_id, top_n: int = 5):
        """Return the top_n items most similar to a given item."""
        idx = self._id_to_index[item_id]
        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        results = []
        for other_idx, score in scores:
            other_id = self.items.iloc[other_idx][self.id_col]
            if other_id == item_id:
                continue
            results.append((other_id, score))
            if len(results) >= top_n:
                break
        return results

    def recommend_for_user(self, liked_item_ids: list, top_n: int = 5):
        """
        Recommend items for a user based on a list of items they liked.
        Averages similarity scores across all liked items, then excludes
        items the user has already seen.
        """
        liked_indices = [self._id_to_index[i] for i in liked_item_ids if i in self._id_to_index]
        if not liked_indices:
            return []

        avg_scores = self.similarity_matrix[liked_indices].mean(axis=0)

        scored_items = []
        for idx, score in enumerate(avg_scores):
            item_id = self.items.iloc[idx][self.id_col]
            if item_id in liked_item_ids:
                continue
            scored_items.append((item_id, score))

        scored_items.sort(key=lambda x: x[1], reverse=True)
        return scored_items[:top_n]

    def get_title(self, item_id, title_col="title"):
        row = self.items[self.items[self.id_col] == item_id]
        return row.iloc[0][title_col] if not row.empty else str(item_id)


# 3. Demo

if __name__ == "__main__":
    recommender = ContentBasedRecommender(
        items=movies,
        id_col="movie_id",
        text_cols=["genre", "description"],
    )

    print("=== Similar movies to 'The Matrix' ===")
    for movie_id, score in recommender.similar_items(item_id=1, top_n=3):
        print(f"  {recommender.get_title(movie_id):20s} (similarity: {score:.3f})")

    print()
    for user, liked in user_ratings.items():
        liked_titles = [recommender.get_title(i) for i in liked]
        print(f"=== Recommendations for {user} (liked: {liked_titles}) ===")
        recs = recommender.recommend_for_user(liked, top_n=3)
        for movie_id, score in recs:
            print(f"  {recommender.get_title(movie_id):20s} (score: {score:.3f})")
        print()
