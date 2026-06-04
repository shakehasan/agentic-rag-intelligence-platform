from __future__ import annotations

import hashlib
import math
import re
from collections.abc import Iterable

TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


class HashingEmbeddingModel:
    """Deterministic local embeddings for a no-key demo runtime.

    The interface mirrors an embedding provider, so a hosted embedding model can replace it
    without changing retrieval code.
    """

    def __init__(self, dimensions: int = 384) -> None:
        self.dimensions = dimensions

    def embed_query(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in tokenize(text):
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            value = int.from_bytes(digest, byteorder="big", signed=False)
            index = value % self.dimensions
            sign = 1.0 if value % 2 == 0 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def embed_documents(self, texts: Iterable[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left)) or 1.0
    right_norm = math.sqrt(sum(b * b for b in right)) or 1.0
    return dot / (left_norm * right_norm)

