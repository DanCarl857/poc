from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas import Chunk


class Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform([chunk.content for chunk in chunks])

    def search(self, question: str, top_k: int = 5) -> list[Chunk]:
        query_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(query_vec, self.matrix).flatten()

        ranked_indices = scores.argsort()[::-1][:top_k]
        return [self.chunks[i] for i in ranked_indices if scores[i] > 0]