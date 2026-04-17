#!/usr/bin/env python3
"""
run_pipeline.py
===============
Main entry point for the Job Skills Intelligence Pipeline.

Flow for each industry:
  1. Discover top N jobs (Anthropic API + web_search, or seed data)
  2. For each job, fetch standard skills + linked tech skills
  3. Merge & score skills (frequency × rank formula)
  4. Cache all API responses (TTL configurable)
  5. Render a single self-contained HTML dashboard (all industries, tabbed)
  6. Write structured run log (JSONL)

Run via cron:
  0 6 * * 1  cd /path/to/job_skills_project && python run_pipeline.py >> logs/cron.log 2>&1

Usage:
  python run_pipeline.py                        # all 6 industries, use cache
  python run_pipeline.py --industries data_ai it_cyber
  python run_pipeline.py --refresh              # ignore cache, re-fetch everything
  python run_pipeline.py --dry-run              # use built-in seed data (no API key)
  python run_pipeline.py --purge-cache          # delete stale cache entries then run
  python run_pipeline.py --list-industries      # print registry and exit
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

# ── make src/ importable when run from project root ──────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from src.config   import (INDUSTRY_REGISTRY, INDUSTRY_PALETTES,
                           JOB_CARD_ACCENTS, SEED_DATA,
                           CACHE_TTL_HOURS, TOP_JOBS, TOP_STD_SKILLS,
                           TOP_TECH_SKILLS, API_RETRIES, MODEL)
from src          import cache as Cache
from src.analyzer import build_job_record
from src.renderer import render_dashboard, write_dashboard
from src.logger   import RunLogger

# ──────────────────────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("skills_pipeline")


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _get_api_key(args_key: str | None) -> str | None:
    return args_key or os.getenv("ANTHROPIC_API_KEY")


def _seed_jobs_for(industry_key: str) -> list[dict]:
    """Return mock job-discovery output from config seed_jobs list."""
    cfg   = INDUSTRY_REGISTRY[industry_key]
    jobs  = cfg.get("seed_jobs", [])
    label = cfg["label"]
    return [
        {
            "posting_rank":        i + 1,
            "job_title":           title,
            "median_salary_usd":   SEED_DATA.get(title, {}).get("median_salary_usd", "N/A"),
            "employment_growth":   SEED_DATA.get(title, {}).get("employment_growth", "N/A"),
        }
        for i, title in enumerate(jobs[:TOP_JOBS])
    ]


def _fetch_with_fallback(
    job_title: str,
    industry_label: str,
    region: str,
    api_key: str | None,
    cache_dir: Path,
    force_refresh: bool,
    dry_run: bool,
) -> tuple[dict | None, str]:
    """
    Returns (skills_dict, source) where source ∈ {"cache","api","seed","error"}.
    Priority: cache → api → seed.
    """
    # 1. Cache
    if not force_refresh:
        hit = Cache.load(cache_dir, "skills", job_title, industry_label, region,
                         ttl_hours=CACHE_TTL_HOURS)
        if hit:
            return hit, "cache"

    # 2. Live API
    if api_key and not dry_run:
        try:
            from src.fetcher import fetch_job_skills
            data = fetch_job_skills(
                job_title=job_title,
                industry_label=industry_label,
                region=region,
                top_std=TOP_STD_SKILLS,
                top_tech_per_std=TOP_TECH_SKILLS,
                api_key=api_key,
                model=MODEL,
                retries=API_RETRIES,
            )
            Cache.save(cache_dir, data, "skills", job_title, industry_label, region)
            return data, "api"
        except Exception as exc:
            log.warning("  API failed for '%s': %s — falling back to seed", job_title, exc)

    # 3. Seed
    if job_title in SEED_DATA:
        log.info("  Using seed data for '%s'", job_title)
        return SEED_DATA[job_title], "seed"

    log.warning("  No data at all for '%s' — skipping", job_title)
    return None, "error"


def _discover_jobs(
    industry_key: str,
    api_key: str | None,
    cache_dir: Path,
    force_refresh: bool,
    dry_run: bool,
) -> tuple[list[dict], str]:
    """Discover top jobs. Returns (job_list, source)."""
    cfg    = INDUSTRY_REGISTRY[industry_key]
    label  = cfg["label"]
    region = cfg["region"]

    # Cache check
    if not force_refresh:
        hit = Cache.load(cache_dir, "jobs", industry_key, region, ttl_hours=CACHE_TTL_HOURS)
        if hit:
            return hit, "cache"

    # Live API
    if api_key and not dry_run:
        try:
            from src.fetcher import fetch_top_jobs
            jobs = fetch_top_jobs(
                industry_label=label,
                region=region,
                top_n=TOP_JOBS,
                api_key=api_key,
                model=MODEL,
                retries=API_RETRIES,
            )
            Cache.save(cache_dir, jobs, "jobs", industry_key, region)
            return jobs, "api"
        except Exception as exc:
            log.warning("  Job discovery API failed for '%s': %s — using seed", label, exc)

    # Seed fallback
    return _seed_jobs_for(industry_key), "seed"


# ──────────────────────────────────────────────────────────────────────────────
# Core pipeline
# ──────────────────────────────────────────────────────────────────────────────

def run(
    industry_keys: list[str],
    api_key: str | None,
    cache_dir: Path,
    output_dir: Path,
    log_dir: Path,
    force_refresh: bool,
    dry_run: bool,
) -> Path:
    run_log = RunLogger(log_dir)
    run_log.set_config(
        industries=industry_keys,
        top_jobs=TOP_JOBS,
        top_std_skills=TOP_STD_SKILLS,
        top_tech_skills=TOP_TECH_SKILLS,
        cache_ttl_hours=CACHE_TTL_HOURS,
        model=MODEL,
        dry_run=dry_run,
        force_refresh=force_refresh,
    )

    all_industries: list[dict] = []

    for ind_key in industry_keys:
        cfg    = INDUSTRY_REGISTRY[ind_key]
        label  = cfg["label"]
        region = cfg["region"]
        log.info("══ Industry: %s ══", label)

        # Step 1 — discover jobs
        job_metas, disc_src = _discover_jobs(
            ind_key, api_key, cache_dir, force_refresh, dry_run
        )
        log.info("  Discovered %d jobs [%s]", len(job_metas), disc_src)

        jobs_processed: list[dict] = []
        counts = {"cache": 0, "api": 0, "seed": 0, "error": 0}

        # Step 2 — fetch skills for each job
        for jm in job_metas[:TOP_JOBS]:
            title = jm["job_title"]
            log.info("  ── Job: %s", title)

            skills_raw, src = _fetch_with_fallback(
                title, label, region, api_key, cache_dir, force_refresh, dry_run
            )
            counts[src] += 1

            if skills_raw is None:
                run_log.add_error(f"{ind_key}/{title}", "No data available")
                continue

            # Step 3 — merge & score
            record = build_job_record(
                job_meta=jm,
                skills_raw=skills_raw,
                top_std=TOP_STD_SKILLS,
                top_tech=TOP_TECH_SKILLS,
            )
            jobs_processed.append(record)
            log.info(
                "    ✓  %d std-skills  |  src=%s",
                len(record["standard_skills"]), src
            )

        all_industries.append({
            "key":    ind_key,
            "label":  label,
            "region": region,
            "jobs":   jobs_processed,
        })

        run_log.add_industry(
            key=ind_key, label=label,
            jobs_discovered=len(job_metas),
            jobs_processed=len(jobs_processed),
            from_cache=counts["cache"],
            from_api=counts["api"],
            from_seed=counts["seed"],
        )

    # Step 4 — render dashboard
    log.info("Rendering HTML dashboard …")
    html = render_dashboard(
        all_industries=all_industries,
        palettes=INDUSTRY_PALETTES,
        job_accents=JOB_CARD_ACCENTS,
        run_id=run_log.run_id,
        cache_ttl=CACHE_TTL_HOURS,
    )
    out_path = write_dashboard(html, output_dir, run_log.run_id)
    run_log.set_output(out_path)
    log.info("✅  Dashboard → %s  (%d bytes)", out_path, out_path.stat().st_size)
    log.info("✅  Latest    → %s", out_path.parent / "dashboard_latest.html")

    run_log.finish()
    return out_path


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Job Skills Intelligence Pipeline — automated fetch + viz",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples
--------
  python run_pipeline.py                          # all industries, honour cache
  python run_pipeline.py --industries data_ai     # single industry
  python run_pipeline.py --refresh                # force re-fetch everything
  python run_pipeline.py --dry-run                # use seed data, no API key needed
  python run_pipeline.py --purge-cache --refresh  # clean slate

Cron (weekly, Monday 06:00)
---------------------------
  0 6 * * 1  cd /your/project && python run_pipeline.py >> logs/cron.log 2>&1
""",
    )
    p.add_argument("--industries",   nargs="+", default=None,
                   choices=list(INDUSTRY_REGISTRY.keys()),
                   help="Which industries to process (default: all)")
    p.add_argument("--refresh",      action="store_true",
                   help="Ignore cache, re-fetch from API")
    p.add_argument("--dry-run",      action="store_true",
                   help="Use built-in seed data (no API key required)")
    p.add_argument("--purge-cache",  action="store_true",
                   help="Delete stale cache entries before running")
    p.add_argument("--cache-dir",    default=None,
                   help="Cache directory (default: ./cache)")
    p.add_argument("--output-dir",   default=None,
                   help="Output directory (default: ./output)")
    p.add_argument("--log-dir",      default=None,
                   help="Log directory (default: ./logs)")
    p.add_argument("--api-key",      default=None,
                   help="Anthropic API key (overrides ANTHROPIC_API_KEY env var)")
    p.add_argument("--list-industries", action="store_true",
                   help="Print available industries and exit")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.list_industries:
        print("\nAvailable industries:\n")
        for k, v in INDUSTRY_REGISTRY.items():
            print(f"  {k:<20} {v['label']}")
            print(f"  {'':20} Jobs: {', '.join(v['seed_jobs'])}\n")
        sys.exit(0)

    # Paths
    base       = Path(__file__).parent
    cache_dir  = Path(args.cache_dir  or os.getenv("SKILLS_CACHE_DIR",  base / "cache"))
    output_dir = Path(args.output_dir or os.getenv("SKILLS_OUTPUT_DIR", base / "output"))
    log_dir    = Path(args.log_dir    or os.getenv("SKILLS_LOG_DIR",    base / "logs"))

    # API key
    api_key = _get_api_key(args.api_key)
    if not api_key and not args.dry_run:
        log.warning(
            "No ANTHROPIC_API_KEY found. Running in implicit dry-run mode.\n"
            "  Set:  export ANTHROPIC_API_KEY=sk-ant-...\n"
            "  Or:   python run_pipeline.py --dry-run"
        )
        args.dry_run = True

    # Optional cache purge
    if args.purge_cache:
        deleted = Cache.purge_stale(cache_dir, CACHE_TTL_HOURS)
        log.info("Purged %d stale cache entries", deleted)

    # Industry selection
    industry_keys = args.industries or list(INDUSTRY_REGISTRY.keys())

    log.info("=" * 60)
    log.info("Job Skills Intelligence Pipeline")
    log.info("  Industries : %s", industry_keys)
    log.info("  Top jobs   : %d per industry", TOP_JOBS)
    log.info("  Top skills : %d std  ×  %d tech each", TOP_STD_SKILLS, TOP_TECH_SKILLS)
    log.info("  Mode       : %s", "dry-run (seed)" if args.dry_run else "live API")
    log.info("  Refresh    : %s", args.refresh)
    log.info("  Cache dir  : %s", cache_dir)
    log.info("  Output dir : %s", output_dir)
    log.info("=" * 60)

    out = run(
        industry_keys=industry_keys,
        api_key=api_key,
        cache_dir=cache_dir,
        output_dir=output_dir,
        log_dir=log_dir,
        force_refresh=args.refresh,
        dry_run=args.dry_run,
    )

    print(f"\n🎉  Done!  Open: file://{out.resolve()}\n")


if __name__ == "__main__":
    main()
