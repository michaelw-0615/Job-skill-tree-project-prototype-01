"""
logger.py
=========
Writes one JSON-Lines record per pipeline run to logs/run_log.jsonl.
Each record is a complete audit snapshot: config used, industries processed,
job counts, skill counts, timing, errors.
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("skills_pipeline.logger")


class RunLogger:
    def __init__(self, log_dir: Path):
        self.log_dir  = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = log_dir / "run_log.jsonl"

        self._start    = time.monotonic()
        self._record: dict = {
            "run_id":     datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "started_at": datetime.now(timezone.utc).isoformat(),
            "finished_at": None,
            "duration_s":  None,
            "config":      {},
            "industries":  [],
            "totals":      {"industries": 0, "jobs": 0, "skills_fetched": 0, "errors": 0},
            "errors":      [],
            "output_file": None,
        }

    def set_config(self, **kwargs) -> None:
        self._record["config"].update(kwargs)

    def add_industry(
        self,
        key: str,
        label: str,
        jobs_discovered: int,
        jobs_processed: int,
        from_cache: int,
        from_api: int,
        from_seed: int,
    ) -> None:
        self._record["industries"].append({
            "key":             key,
            "label":           label,
            "jobs_discovered": jobs_discovered,
            "jobs_processed":  jobs_processed,
            "from_cache":      from_cache,
            "from_api":        from_api,
            "from_seed":       from_seed,
        })
        self._record["totals"]["industries"] += 1
        self._record["totals"]["jobs"]       += jobs_processed

    def add_error(self, context: str, message: str) -> None:
        self._record["errors"].append({"context": context, "message": str(message)})
        self._record["totals"]["errors"] += 1
        log.warning("[run-log] ERROR  %s — %s", context, message)

    def set_output(self, path: Path) -> None:
        self._record["output_file"] = str(path)

    def finish(self) -> None:
        elapsed = time.monotonic() - self._start
        self._record["finished_at"] = datetime.now(timezone.utc).isoformat()
        self._record["duration_s"]  = round(elapsed, 2)

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(self._record, ensure_ascii=False) + "\n")

        log.info(
            "Run %s finished in %.1fs — %d industries, %d jobs, %d errors",
            self._record["run_id"],
            elapsed,
            self._record["totals"]["industries"],
            self._record["totals"]["jobs"],
            self._record["totals"]["errors"],
        )

    @property
    def run_id(self) -> str:
        return self._record["run_id"]
