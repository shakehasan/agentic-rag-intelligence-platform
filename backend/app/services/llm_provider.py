from __future__ import annotations

import re
from dataclasses import dataclass

from backend.app.schemas.documents import RetrievedChunk

INSUFFICIENT_CONTEXT_MESSAGE = "I do not have enough context in the indexed documents."

STOPWORDS = {
    "about",
    "after",
    "does",
    "from",
    "have",
    "into",
    "that",
    "the",
    "their",
    "there",
    "this",
    "what",
    "when",
    "where",
    "which",
    "with",
    "would",
    "should",
    "northstar",
    "labs",
}


@dataclass
class GeneratedAnswer:
    answer: str
    confidence: float


class GroundedLLMProvider:
    """LLM-compatible service boundary with a local grounded fallback.

    The fallback is intentionally extractive: it only composes answers from retrieved snippets,
    which makes the demo useful without a remote model key and keeps citations honest.
    """

    def generate_grounded_answer(
        self,
        query: str,
        contexts: list[RetrievedChunk],
        intent: str,
    ) -> GeneratedAnswer:
        if not contexts:
            return GeneratedAnswer(answer=INSUFFICIENT_CONTEXT_MESSAGE, confidence=0.0)

        query_terms = _content_terms(query)
        ranked_sentences: list[tuple[int, float, str]] = []
        for context in contexts:
            text = str(context.metadata.get("content") or context.excerpt)
            for sentence in _sentences(text):
                score = len(query_terms.intersection(_content_terms(sentence)))
                if score:
                    ranked_sentences.append((score, context.score, sentence))

        if not ranked_sentences:
            best = contexts[0]
            text = str(best.metadata.get("content") or best.excerpt)
            first_sentence = _sentences(text)[0] if _sentences(text) else best.excerpt
            return GeneratedAnswer(answer=first_sentence, confidence=min(best.score, 0.55))

        ranked_sentences.sort(key=lambda item: (item[0], item[1]), reverse=True)
        selected = _dedupe_sentences([sentence for _, _, sentence in ranked_sentences[:4]])
        if intent == "comparison":
            answer = "Compared across the retrieved sources, " + " ".join(selected)
        elif intent == "summarization":
            answer = "Summary: " + " ".join(selected)
        else:
            answer = " ".join(selected)
        confidence = sum(context.score for context in contexts[:3]) / min(len(contexts), 3)
        return GeneratedAnswer(answer=answer, confidence=round(min(confidence, 0.98), 2))


def _content_terms(text: str) -> set[str]:
    return {
        token.lower()
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", text)
        if len(token) > 2 and token.lower() not in STOPWORDS
    }


def _sentences(text: str) -> list[str]:
    compact = " ".join(text.split())
    sentences = re.split(r"(?<=[.!?])\s+", compact)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def _dedupe_sentences(sentences: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for sentence in sentences:
        normalized = sentence.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(sentence)
    return unique
