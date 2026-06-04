from __future__ import annotations

DOMAIN_SYNONYMS: dict[str, set[str]] = {
    "governance": {"policy", "review", "responsible ai", "approval"},
    "deployment": {"cloud", "release", "runtime", "rollback"},
    "security": {"authorization", "secret handling", "input validation", "abuse testing"},
    "privacy": {"retention", "minimization", "deletion", "data review"},
    "quality": {"test strategy", "automation", "regression", "validation"},
    "support": {"knowledge article", "triage", "insufficient context", "help desk"},
}


def expand_query_terms(query: str, max_terms: int = 8) -> list[str]:
    lowered = query.lower()
    expansions: list[str] = []
    for anchor, synonyms in DOMAIN_SYNONYMS.items():
        if anchor in lowered:
            expansions.extend(sorted(synonyms))
    return _dedupe(expansions)[:max_terms]


def build_expanded_query(query: str) -> str:
    expansions = expand_query_terms(query)
    if not expansions:
        return query
    return f"{query} {' '.join(expansions)}"


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique

