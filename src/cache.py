"""
cache.py
========
Disk-backed JSON cache keyed by (job_title, industry, region).
Entries expire after CACHE_TTL_HOURS (configurable).
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("skills_pipeline.cache")


def _key(namespace: str, *parts: str) -> str:
    raw = "|".join([namespace] + [p.lower() for p in parts])
    return hashlib.md5(raw.encode()).hexdigest()[:14]


def load(cache_dir: Path, namespace: str, *parts: str, ttl_hours: float) -> dict | None:
    """Return cached dict if present and fresh, else None."""
    key  = _key(namespace, *parts)
    path = cache_dir / f"{key}.json"
    if not path.exists():
        return None
    try:
        payload  = json.loads(path.read_text(encoding="utf-8"))
        saved_at = datetime.fromisoformat(payload["_saved_at"])
        age_h    = (datetime.now(timezone.utc) - saved_at).total_seconds() / 3600
        if age_h < ttl_hours:
            log.debug("Cache HIT  %s  (age=%.1fh)", path.name, age_h)
            return payload["data"]
        log.debug("Cache STALE %s  (age=%.1fh)", path.name, age_h)
    except Exception as exc:
        log.warning("Cache read error %s: %s", path.name, exc)
    return None


def save(cache_dir: Path, data: dict, namespace: str, *parts: str) -> None:
    """Persist data to cache."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    key  = _key(namespace, *parts)
    path = cache_dir / f"{key}.json"
    payload = {"_saved_at": datetime.now(timezone.utc).isoformat(), "data": data}
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    log.debug("Cache SAVE %s", path.name)


def invalidate(cache_dir: Path, namespace: str, *parts: str) -> bool:
    """Delete a cache entry. Returns True if the file existed."""
    key  = _key(namespace, *parts)
    path = cache_dir / f"{key}.json"
    if path.exists():
        path.unlink()
        log.info("Cache INVALIDATED %s", path.name)
        return True
    return False


def purge_stale(cache_dir: Path, ttl_hours: float) -> int:
    """Delete all stale entries. Returns count deleted."""
    if not cache_dir.exists():
        return 0
    deleted = 0
    for path in cache_dir.glob("*.json"):
        try:
            payload  = json.loads(path.read_text(encoding="utf-8"))
            saved_at = datetime.fromisoformat(payload["_saved_at"])
            age_h    = (datetime.now(timezone.utc) - saved_at).total_seconds() / 3600
            if age_h >= ttl_hours:
                path.unlink()
                deleted += 1
        except Exception:
            pass
    if deleted:
        log.info("Purged %d stale cache entries", deleted)
    return deleted
