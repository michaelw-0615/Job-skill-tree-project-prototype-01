# Job-skill-tree-project-prototype-01

This is an automated, cron-ready pipeline that:
1. **Discovers** the top 5 most-posted jobs per industry via Anthropic web search
2. **Fetches** the top 5 standard skills per job, each linked to 3–5 tech skills
3. **Scores & merges** skill signals using a weighted frequency/rank formula
4. **Caches** all API results (72h TTL) to minimise token spend on re-runs
5. **Renders** a self-contained, interactive HTML dashboard (all 6 industries, one page)
6. **Logs** every run with structured JSON for audit/trend tracking

## Industries covered (as of Apr 17, 2026)
| Key | Industry |
|-----|----------|
| `transportation` | Transportation / Logistics / Supply Chain |
| `data_ai` | Data / AI |
| `it_cyber` | IT / Cybersecurity |
| `healthcare` | Healthcare |
| `manufacturing` | Manufacturing |
| `energy` | Energy & Sustainability |

## Project layout
```
job_skills_project/
├── README.md
├── requirements.txt
├── run_pipeline.py          ← main entry point (run this)
├── src/
│   ├── config.py            ← industry registry & palette definitions
│   ├── fetcher.py           ← Anthropic API calls + web_search
│   ├── cache.py             ← JSON cache with TTL
│   ├── analyzer.py          ← skill normalisation, merge & scoring
│   ├── renderer.py          ← HTML dashboard template & injection
│   └── logger.py            ← structured run-log writer
├── cache/                   ← auto-created: timestamped JSON responses
├── output/                  ← auto-created: dated HTML dashboards
└── logs/                    ← auto-created: run_log.jsonl
```

## Prerequisites
- A valid Claude API key for automated fetching and analysis (different from Claude chatbot, subscribe [here](https://claude.com/pricing#api)).
- Python>=3.12

## Quick start
```bash
# 0. Configure (If Python is already installed globally)
python -m venv --system-site-packages .venv
.\.venv\Scripts\Activate.ps1

# 1. Install
pip install anthropic

# 2. Set API key
export ANTHROPIC_API_KEY=sk-ant-...
# For Powershell, enter the following:
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# 3. Run (all 6 industries)
python run_pipeline.py

# 4. Run a single industry
python run_pipeline.py --industries transportation

# 5. Force fresh search (ignore cache)
python run_pipeline.py --refresh

# 6. Dry-run with seed data (no API key needed)
python run_pipeline.py --dry-run
```

## Cron setup
Add to crontab (`crontab -e`) to run every Monday at 06:00:
```
0 6 * * 1  cd /path/to/job_skills_project && python run_pipeline.py >> logs/cron.log 2>&1
```

Or daily at 05:00:
```
0 5 * * *  cd /path/to/job_skills_project && python run_pipeline.py --refresh >> logs/cron.log 2>&1
```

