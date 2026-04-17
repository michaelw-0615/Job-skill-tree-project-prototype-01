"""
analyzer.py
===========
Skill normalisation, deduplication, and importance scoring.

Scoring formula (0–100):
    importance = 0.55 * mention_score + 0.45 * rank_score

Where:
    mention_score = (mean_mentions / 10) * 100        # citation breadth
    rank_score    = ((N+1 - mean_rank) / N) * 100     # ranking signal
    N             = highest rank observed in the list
"""

from __future__ import annotations

import re
from collections import defaultdict


def normalise(name: str) -> str:
    """Lowercase + strip punctuation for fuzzy deduplication."""
    return re.sub(r"[^a-z0-9 ]", "", name.lower()).strip()


def score_skill(mean_mentions: float, mean_rank: float, max_rank: int) -> int:
    mention_score = (mean_mentions / 10) * 100
    rank_score    = ((max_rank + 1 - mean_rank) / max_rank) * 100
    raw = 0.55 * mention_score + 0.45 * rank_score
    return max(1, min(100, round(raw)))


def merge_skill_list(skills: list[dict]) -> list[dict]:
    """
    Deduplicate + score a flat list of skill dicts.
    Each dict must have: name, mentions, rank.
    Returns sorted list with 'importance' field added and consecutive ranks.
    """
    if not skills:
        return []

    groups: dict[str, list[dict]] = defaultdict(list)
    for s in skills:
        groups[normalise(s["name"])].append(s)

    max_rank = max(s["rank"] for s in skills)
    merged   = []

    for items in groups.values():
        canonical    = max(items, key=lambda x: len(x["name"]))["name"]
        mean_ment    = sum(i.get("mentions", 5) for i in items) / len(items)
        mean_rank_v  = sum(i["rank"] for i in items) / len(items)
        importance   = score_skill(mean_ment, mean_rank_v, max_rank)
        merged.append({
            "name":       canonical,
            "importance": importance,
            "_sort_key":  (mean_rank_v, -importance),
        })

    merged.sort(key=lambda x: x["_sort_key"])
    for i, s in enumerate(merged, 1):
        s["rank"] = i
        del s["_sort_key"]

    return merged


def merge_tech_skills(tech_skills: list[dict]) -> list[dict]:
    """Same as merge_skill_list but for tech skill sub-lists."""
    return merge_skill_list(tech_skills)


def build_job_record(
    job_meta: dict,
    skills_raw: dict,
    top_std: int,
    top_tech: int,
) -> dict:
    """
    Combine job metadata (from discovery) with skill data (from skills fetch).
    Returns a clean dict ready for the renderer.

    job_meta keys:  posting_rank, job_title, median_salary_usd, employment_growth
    skills_raw keys: standard_skills (each with tech_skills sub-list), sources
    """
    std_raw = skills_raw.get("standard_skills", [])

    # Merge/score each standard skill's tech sub-list
    processed_std = []
    for s in std_raw[:top_std]:
        merged_tech = merge_tech_skills(s.get("tech_skills", []))[:top_tech]
        # re-rank after trimming
        for i, t in enumerate(merged_tech, 1):
            t["rank"] = i
        processed_std.append({
            "name":       s["name"],
            "rank":       s.get("rank", len(processed_std) + 1),
            "mentions":   s.get("mentions", 5),
            "tech_skills": merged_tech,
        })

    # Score and re-rank the standard skills themselves
    flat_std = [{"name": s["name"], "mentions": s["mentions"], "rank": s["rank"]}
                for s in processed_std]
    scored_std = merge_skill_list(flat_std)

    # Re-attach tech_skills using original order mapping
    tech_map = {normalise(s["name"]): s["tech_skills"] for s in processed_std}
    for s in scored_std:
        s["tech_skills"] = tech_map.get(normalise(s["name"]), [])

    return {
        "posting_rank":      job_meta.get("posting_rank", 0),
        "title":             job_meta.get("job_title", skills_raw.get("job_title", "?")),
        "median_salary":     job_meta.get("median_salary_usd", "N/A"),
        "growth":            job_meta.get("employment_growth", "N/A"),
        "standard_skills":   scored_std[:top_std],
        "sources":           skills_raw.get("sources", []),
    }
