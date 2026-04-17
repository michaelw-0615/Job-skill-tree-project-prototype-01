"""
fetcher.py
==========
Two-stage Anthropic API fetch:
  Stage 1 – discover the top N most-posted jobs for an industry (web_search)
  Stage 2 – for each job, fetch top standard skills + linked tech skills
"""

from __future__ import annotations

import json
import logging
import re
import time
from datetime import datetime, timezone

log = logging.getLogger("skills_pipeline.fetcher")


# ──────────────────────────────────────────────────────────────────────────────
# Prompt builders
# ──────────────────────────────────────────────────────────────────────────────

def _prompt_discover_jobs(industry_label: str, region: str, top_n: int) -> str:
    year = datetime.now(timezone.utc).year
    return f"""You are a labour-market research analyst.

Search the web for the most recent ({year}) job-posting data for the
"{industry_label}" industry in {region}.

Return ONLY valid JSON (no markdown, no prose) with this exact schema:
{{
  "industry": "{industry_label}",
  "region": "{region}",
  "data_year": "{year}",
  "top_jobs": [
    {{
      "posting_rank": 1,
      "job_title": "<most posted job title>",
      "median_salary_usd": "<e.g. $95,000–$120,000>",
      "employment_growth": "<e.g. +12% (2024-2034)>"
    }},
    ...
  ]
}}

Rules:
- Provide exactly {top_n} jobs ranked by number of job postings (most first)
- Use current job titles as they appear on LinkedIn, Indeed, Glassdoor, BLS
- Prioritise BLS O*NET, LinkedIn Talent Insights, Indeed Hiring Lab data
- If salary is unavailable, write "N/A"
"""


def _prompt_job_skills(
    job_title: str,
    industry_label: str,
    region: str,
    top_std: int,
    top_tech_per_std: int,
) -> str:
    year = datetime.now(timezone.utc).year
    return f"""You are a labour-market research analyst.

Search the web for current ({year}) skill requirements for "{job_title}"
in the "{industry_label}" industry in {region}.

Return ONLY valid JSON (no markdown, no prose):
{{
  "job_title": "{job_title}",
  "standard_skills": [
    {{
      "name": "<standard skill name>",
      "mentions": <int 1-10>,
      "rank": <1-based int>,
      "tech_skills": [
        {{"name": "<specific tool/software/platform>", "mentions": <int 1-10>, "rank": <1-based int>}},
        ...
      ]
    }},
    ...
  ],
  "sources": ["<url or source name>", ...]
}}

Rules:
- standard_skills = foundational/interpersonal/cognitive skills
  (e.g. communication, analytical thinking, leadership, attention to detail)
- tech_skills under each standard skill = the 3–{top_tech_per_std} most relevant
  specific tools / software / platforms / certifications for THAT skill
- Provide exactly {top_std} standard skills, each with 3–{top_tech_per_std} tech skills
- "mentions" = number of sources (1–10) that highlighted this skill
- Rank by importance within each list
- Prioritise BLS O*NET, LinkedIn, Glassdoor, Indeed, industry bodies
"""


# ──────────────────────────────────────────────────────────────────────────────
# API caller
# ──────────────────────────────────────────────────────────────────────────────

def _call_claude(prompt: str, api_key: str, model: str, retries: int = 3) -> str:
    """Call Claude with web_search enabled; return raw text."""
    try:
        import anthropic
    except ImportError:
        raise ImportError("Run:  pip install anthropic")

    client = anthropic.Anthropic(api_key=api_key)

    for attempt in range(1, retries + 1):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=2048,
                tools=[{"type": "web_search_20250305", "name": "web_search"}],
                messages=[{"role": "user", "content": prompt}],
            )
            return "\n".join(
                b.text for b in response.content if hasattr(b, "text")
            ).strip()
        except Exception as exc:
            log.warning("API attempt %d/%d failed: %s", attempt, retries, exc)
            if attempt < retries:
                time.sleep(2 ** attempt)
            else:
                raise


def _parse_json(raw: str) -> dict:
    """Strip any markdown fences and parse JSON."""
    cleaned = re.sub(r"^```[a-z]*\n?", "", raw.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\n?```$", "", cleaned.strip(), flags=re.MULTILINE)
    # Find first '{' and last '}' in case Claude prefixed/suffixed text
    start = cleaned.find("{")
    end   = cleaned.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON object found in response:\n{raw[:400]}")
    return json.loads(cleaned[start:end])


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def fetch_top_jobs(
    industry_label: str,
    region: str,
    top_n: int,
    api_key: str,
    model: str,
    retries: int = 3,
) -> list[dict]:
    """
    Stage 1: discover the top N posted jobs for an industry.
    Returns list of dicts: [{posting_rank, job_title, median_salary_usd, employment_growth}, ...]
    """
    log.info("  [fetch] Discovering top %d jobs for '%s' …", top_n, industry_label)
    prompt = _prompt_discover_jobs(industry_label, region, top_n)
    raw = _call_claude(prompt, api_key, model, retries)
    data = _parse_json(raw)
    jobs = data.get("top_jobs", [])
    log.info("  [fetch] Found %d jobs", len(jobs))
    return jobs


def fetch_job_skills(
    job_title: str,
    industry_label: str,
    region: str,
    top_std: int,
    top_tech_per_std: int,
    api_key: str,
    model: str,
    retries: int = 3,
) -> dict:
    """
    Stage 2: fetch standard skills + linked tech skills for a job.
    Returns the parsed JSON dict.
    """
    log.info("  [fetch] Skills for '%s' …", job_title)
    prompt = _prompt_job_skills(job_title, industry_label, region, top_std, top_tech_per_std)
    raw = _call_claude(prompt, api_key, model, retries)
    data = _parse_json(raw)
    return data
