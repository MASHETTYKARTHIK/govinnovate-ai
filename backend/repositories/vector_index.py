"""Small deterministic FAISS-style vector index for local JSON records."""

import math
import re
from collections import Counter


class MockFaissIndex:
    """Rank text records using normalized bag-of-words cosine similarity."""

    def __init__(self, documents: list[str]) -> None:
        self.vectors = [self._vectorize(document) for document in documents]

    def search(self, query: str, limit: int = 10) -> list[tuple[int, float]]:
        """Return document indexes and cosine similarity scores."""
        query_vector = self._vectorize(query)
        scores = [
            (index, self._cosine(query_vector, vector))
            for index, vector in enumerate(self.vectors)
        ]
        return sorted(scores, key=lambda item: item[1], reverse=True)[:limit]

    @staticmethod
    def _vectorize(text: str) -> Counter[str]:
        return Counter(re.findall(r"[a-z0-9]{3,}", text.lower()))

    @staticmethod
    def _cosine(left: Counter[str], right: Counter[str]) -> float:
        shared = left.keys() & right.keys()
        numerator = sum(left[word] * right[word] for word in shared)
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0
