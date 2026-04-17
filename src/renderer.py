"""
renderer.py
===========
Generates a self-contained, single-file HTML dashboard.
Layout: tabbed by industry → job cards → expandable skill trees.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# HTML template (inline CSS + JS, zero external dependencies beyond Google Fonts)
# ──────────────────────────────────────────────────────────────────────────────

_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Job Skills Intelligence Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Sora:wght@300;400;600;700;800&display=swap" rel="stylesheet"/>
<style>
/* ── Reset ── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}

/* ── Root vars ── */
:root{
  --bg:#080c14;--surface:#0f1623;--surface2:#151e2e;--border:rgba(255,255,255,0.07);
  --text:#e2e8f0;--muted:#64748b;--muted2:#475569;
  --radius:14px;--tab-h:48px;
}

/* ── Base ── */
body{background:var(--bg);color:var(--text);font-family:'Sora',sans-serif;
  min-height:100vh;overflow-x:hidden;}

/* starfield */
body::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:
    radial-gradient(1px 1px at 15% 25%,rgba(255,255,255,.18),transparent),
    radial-gradient(1px 1px at 75% 8%, rgba(255,255,255,.12),transparent),
    radial-gradient(1px 1px at 45% 65%,rgba(255,255,255,.10),transparent),
    radial-gradient(1px 1px at 88% 55%,rgba(255,255,255,.08),transparent),
    radial-gradient(1px 1px at 30% 90%,rgba(255,255,255,.12),transparent),
    radial-gradient(1px 1px at 60% 40%,rgba(255,255,255,.07),transparent);}

.page{position:relative;z-index:1;max-width:1480px;margin:0 auto;padding:40px 20px 80px;}

/* ── Header ── */
.site-header{text-align:center;margin-bottom:48px;}
.site-badge{display:inline-flex;align-items:center;gap:8px;
  background:rgba(255,255,255,.05);border:1px solid var(--border);border-radius:999px;
  padding:6px 18px;font-size:.7rem;letter-spacing:.13em;text-transform:uppercase;
  color:var(--muted);margin-bottom:18px;font-family:'DM Mono',monospace;}
.site-header h1{font-size:clamp(1.8rem,4.5vw,3rem);font-weight:800;letter-spacing:-.03em;
  background:linear-gradient(135deg,#f1f5f9 20%,#64748b);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.site-header p{margin-top:10px;color:var(--muted);font-size:.9rem;font-weight:300;}
.run-meta{margin-top:8px;font-family:'DM Mono',monospace;font-size:.66rem;color:var(--muted2);}

/* ── Industry tabs ── */
.tabs-wrap{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:32px;justify-content:center;}
.tab-btn{
  display:flex;align-items:center;gap:8px;
  padding:10px 20px;border-radius:999px;border:1px solid var(--border);
  background:rgba(255,255,255,.04);color:var(--muted);cursor:pointer;
  font-family:'Sora',sans-serif;font-size:.82rem;font-weight:600;
  transition:all .25s ease;white-space:nowrap;
}
.tab-btn:hover{background:rgba(255,255,255,.08);color:var(--text);}
.tab-btn.active{color:#fff;border-color:transparent;}

/* ── Industry panel ── */
.industry-panel{display:none;}
.industry-panel.active{display:block;}

.industry-header{
  display:flex;align-items:center;gap:16px;
  margin-bottom:28px;padding:20px 28px;
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  border-left:4px solid var(--ind-primary,#60a5fa);
}
.ind-emoji{font-size:2.2rem;}
.ind-title{font-size:1.3rem;font-weight:700;letter-spacing:-.02em;}
.ind-sub{font-size:.78rem;color:var(--muted);margin-top:4px;font-family:'DM Mono',monospace;}

/* ── Jobs grid ── */
.jobs-grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
  gap:20px;
}

/* ── Job card ── */
.job-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.35);
  transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease;
}
.job-card:hover{transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,0,0,.55);}

.job-card-header{
  padding:18px 20px 14px;border-bottom:1px solid var(--border);
  background:linear-gradient(135deg,var(--job-color,rgba(96,165,250,.12)),transparent);
  position:relative;
}
.job-rank-badge{
  position:absolute;top:14px;right:16px;
  font-family:'DM Mono',monospace;font-size:.65rem;color:var(--muted);
  background:rgba(255,255,255,.06);padding:2px 8px;border-radius:999px;
}
.job-title{font-size:.98rem;font-weight:700;letter-spacing:-.02em;
  color:var(--job-accent,#93c5fd);margin-bottom:10px;}
.job-pills{display:flex;flex-wrap:wrap;gap:6px;}
.pill{font-family:'DM Mono',monospace;font-size:.66rem;padding:3px 10px;
  border-radius:999px;white-space:nowrap;}
.pill-salary{background:rgba(255,255,255,.07);color:#94a3b8;}
.pill-growth{background:rgba(74,222,128,.1);color:#4ade80;}

/* ── Skill tree inside card ── */
.skill-tree{padding:16px 18px 12px;}

.std-skill{margin-bottom:14px;border-radius:10px;overflow:hidden;
  border:1px solid rgba(255,255,255,.05);}
.std-skill-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:9px 14px;cursor:pointer;
  background:rgba(255,255,255,.03);
  transition:background .2s;
  user-select:none;
}
.std-skill-header:hover{background:rgba(255,255,255,.06);}
.std-skill-left{display:flex;align-items:center;gap:10px;}
.std-skill-name{font-size:.82rem;font-weight:600;color:var(--text);}
.std-importance{font-family:'DM Mono',monospace;font-size:.62rem;color:var(--muted);}
.std-bar-wrap{flex:1;height:3px;background:rgba(255,255,255,.06);border-radius:999px;
  margin:0 12px;overflow:hidden;min-width:40px;}
.std-bar{height:100%;border-radius:999px;background:var(--ind-secondary,#93c5fd);
  transition:width .7s cubic-bezier(.16,1,.3,1);}
.chevron{font-size:.7rem;color:var(--muted);transition:transform .25s;}
.chevron.open{transform:rotate(90deg);}

/* tech skills sub-list */
.tech-list{display:none;padding:8px 14px 12px;background:rgba(0,0,0,.18);}
.tech-list.visible{display:block;}
.tech-item{display:flex;align-items:center;gap:10px;padding:5px 0;
  border-bottom:1px solid rgba(255,255,255,.04);}
.tech-item:last-child{border-bottom:none;}
.tech-rank{font-family:'DM Mono',monospace;font-size:.6rem;color:var(--muted);
  min-width:18px;text-align:right;}
.tech-name{font-size:.76rem;color:#cbd5e1;flex:1;}
.tech-bar-wrap{width:60px;height:3px;background:rgba(255,255,255,.06);
  border-radius:999px;overflow:hidden;}
.tech-bar{height:100%;border-radius:999px;
  background:var(--ind-accent,#818cf8);
  transition:width .7s cubic-bezier(.16,1,.3,1);}
.tech-imp{font-family:'DM Mono',monospace;font-size:.58rem;color:var(--muted);
  min-width:28px;text-align:right;}

/* sources */
.job-sources{padding:8px 18px 14px;}
.src-toggle{font-size:.62rem;color:var(--muted2);cursor:pointer;font-family:'DM Mono',monospace;
  display:inline-flex;align-items:center;gap:4px;}
.src-toggle:hover{color:#94a3b8;}
.src-list{display:none;margin-top:6px;}
.src-list a{display:block;font-size:.58rem;color:#475569;font-family:'DM Mono',monospace;
  text-decoration:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  margin-bottom:3px;}
.src-list a:hover{color:#94a3b8;}

/* ── Legend ── */
.legend{margin:48px auto 0;max-width:640px;display:flex;justify-content:center;
  flex-wrap:wrap;gap:24px;}
.leg-item{display:flex;align-items:center;gap:8px;font-size:.76rem;color:var(--muted);}
.leg-dot{width:10px;height:10px;border-radius:50%;}

/* ── Footer ── */
.site-footer{margin-top:40px;text-align:center;font-size:.65rem;
  color:var(--muted2);font-family:'DM Mono',monospace;line-height:2;}

@media(max-width:680px){
  .jobs-grid{grid-template-columns:1fr;}
  .tabs-wrap{gap:6px;}
  .tab-btn{padding:8px 14px;font-size:.76rem;}
}
</style>
</head>
<body>
<div class="page">

  <!-- Header -->
  <header class="site-header">
    <div class="site-badge">🇺🇸 United States &nbsp;·&nbsp; Job Skills Intelligence</div>
    <h1>Industry Skills Dashboard</h1>
    <p>Top 5 jobs &nbsp;·&nbsp; Top 5 standard skills &nbsp;·&nbsp; 3–5 tech skills per standard skill</p>
    <div class="run-meta">
      Generated __NOW__ &nbsp;|&nbsp; Model: claude-sonnet-4-5 + web_search &nbsp;|&nbsp;
      Cache TTL: __TTL__h &nbsp;|&nbsp; Run ID: __RUN_ID__
    </div>
  </header>

  <!-- Tabs -->
  <div class="tabs-wrap" id="tabs"></div>

  <!-- Industry panels -->
  <div id="panels"></div>

  <!-- Legend -->
  <div class="legend">
    <div class="leg-item"><div class="leg-dot" style="background:#93c5fd"></div>Standard skill (click to expand)</div>
    <div class="leg-item"><div class="leg-dot" style="background:#86efac"></div>Linked technology skills</div>
    <div class="leg-item"><div class="leg-dot" style="background:#fde68a"></div>Bar width = importance score (0–100)</div>
  </div>

  <!-- Footer -->
  <footer class="site-footer">
    Pipeline: run_pipeline.py &nbsp;|&nbsp;
    Scoring: 55% mention-frequency + 45% rank-weighted &nbsp;|&nbsp;
    Sources: BLS O*NET · LinkedIn · Indeed · Glassdoor · Industry Associations
  </footer>

</div>

<script>
const INDUSTRIES = __INDUSTRIES_JSON__;

// ── colour registration ──────────────────────────────────────────────────────
const IND_PALETTES = __PALETTES_JSON__;
const JOB_ACCENTS  = __JOB_ACCENTS_JSON__;

// ── Tab bar ─────────────────────────────────────────────────────────────────
const tabsEl   = document.getElementById('tabs');
const panelsEl = document.getElementById('panels');

INDUSTRIES.forEach((ind, i) => {
  const pal = IND_PALETTES[ind.key] || {};

  // tab button
  const btn = document.createElement('button');
  btn.className = 'tab-btn' + (i === 0 ? ' active' : '');
  btn.dataset.idx = i;
  btn.style.cssText = i === 0
    ? `background:${pal.primary};color:#fff;box-shadow:0 0 20px ${pal.glow};`
    : '';
  btn.innerHTML = `<span>${pal.emoji||'🏭'}</span> ${ind.label}`;
  btn.onclick = () => switchTab(i);
  tabsEl.appendChild(btn);

  // panel
  const panel = document.createElement('div');
  panel.className = 'industry-panel' + (i === 0 ? ' active' : '');
  panel.id = `panel-${i}`;
  panel.style.setProperty('--ind-primary',    pal.primary   || '#60a5fa');
  panel.style.setProperty('--ind-secondary',  pal.secondary || '#93c5fd');
  panel.style.setProperty('--ind-accent',     pal.accent    || '#6366f1');
  panel.style.setProperty('--ind-glow',       pal.glow      || 'rgba(96,165,250,0.2)');
  panel.innerHTML = buildIndustryPanel(ind, pal);
  panelsEl.appendChild(panel);
});

// ── Tab switch ───────────────────────────────────────────────────────────────
function switchTab(idx) {
  document.querySelectorAll('.tab-btn').forEach((b, i) => {
    const pal = IND_PALETTES[INDUSTRIES[i].key] || {};
    b.classList.toggle('active', i === idx);
    b.style.cssText = i === idx
      ? `background:${pal.primary};color:#fff;box-shadow:0 0 20px ${pal.glow};`
      : '';
  });
  document.querySelectorAll('.industry-panel').forEach((p, i) => {
    p.classList.toggle('active', i === idx);
  });
  // Animate bars in newly visible panel
  setTimeout(() => animateBars(`#panel-${idx}`), 50);
}

// ── HTML builders ────────────────────────────────────────────────────────────
function buildIndustryPanel(ind, pal) {
  const header = `
    <div class="industry-header">
      <span class="ind-emoji">${pal.emoji||'🏭'}</span>
      <div>
        <div class="ind-title">${ind.label}</div>
        <div class="ind-sub">Top ${ind.jobs.length} jobs by posting volume &nbsp;·&nbsp; ${ind.region}</div>
      </div>
    </div>`;

  const cards = ind.jobs.map((job, ji) => buildJobCard(job, ji, pal)).join('');
  return header + `<div class="jobs-grid">${cards}</div>`;
}

function buildJobCard(job, ji, pal) {
  const accent = JOB_ACCENTS[ji % JOB_ACCENTS.length];
  const colorHex = pal.primary || '#60a5fa';
  const stdSkills = job.standard_skills.map((s, si) => buildStdSkill(s, si, pal)).join('');

  const srcHtml = (job.sources||[]).length > 0
    ? `<div class="job-sources">
         <span class="src-toggle" onclick="toggleSrc(this)">🔗 ${job.sources.length} source${job.sources.length>1?'s':''} ▸</span>
         <div class="src-list">${job.sources.map(u=>`<a href="${u}" target="_blank" rel="noopener">${u}</a>`).join('')}</div>
       </div>`
    : '';

  return `
  <div class="job-card" style="--job-color:${colorHex}1a;--job-accent:${accent}">
    <div class="job-card-header">
      <div class="job-rank-badge">#${job.posting_rank} by postings</div>
      <div class="job-title">${job.title}</div>
      <div class="job-pills">
        <span class="pill pill-salary">💰 ${job.median_salary||'N/A'}</span>
        <span class="pill pill-growth">📈 ${job.growth||'N/A'}</span>
      </div>
    </div>
    <div class="skill-tree">${stdSkills}</div>
    ${srcHtml}
  </div>`;
}

function buildStdSkill(s, si, pal) {
  const imp = s.importance || 70;
  const techItems = (s.tech_skills||[]).map(t => {
    const timp = t.importance || 65;
    return `
    <div class="tech-item">
      <span class="tech-rank">${t.rank}</span>
      <span class="tech-name">${t.name}</span>
      <div class="tech-bar-wrap">
        <div class="tech-bar" data-w="${timp}" style="width:0%"></div>
      </div>
      <span class="tech-imp">${timp}%</span>
    </div>`;
  }).join('');

  return `
  <div class="std-skill">
    <div class="std-skill-header" onclick="toggleSkill(this)">
      <div class="std-skill-left">
        <span class="std-skill-name">${s.name}</span>
        <span class="std-importance">${imp}%</span>
      </div>
      <div class="std-bar-wrap">
        <div class="std-bar" data-w="${imp}" style="width:0%"></div>
      </div>
      <span class="chevron">▶</span>
    </div>
    <div class="tech-list">${techItems}</div>
  </div>`;
}

// ── Interactions ─────────────────────────────────────────────────────────────
function toggleSkill(header) {
  const chevron  = header.querySelector('.chevron');
  const techList = header.nextElementSibling;
  const isOpen   = techList.classList.contains('visible');
  techList.classList.toggle('visible', !isOpen);
  chevron.classList.toggle('open', !isOpen);
}

function toggleSrc(toggle) {
  const list = toggle.nextElementSibling;
  const open = list.style.display === 'block';
  list.style.display = open ? 'none' : 'block';
  toggle.textContent = toggle.textContent.replace(open ? '▾' : '▸', open ? '▸' : '▾');
}

// ── Bar animation ─────────────────────────────────────────────────────────────
function animateBars(scope) {
  document.querySelectorAll(`${scope} [data-w]`).forEach(el => {
    el.style.width = el.dataset.w + '%';
  });
}

// Animate first panel on load
setTimeout(() => animateBars('#panel-0'), 150);
</script>
</body>
</html>
"""


# ──────────────────────────────────────────────────────────────────────────────
# Public render function
# ──────────────────────────────────────────────────────────────────────────────

def render_dashboard(
    all_industries: list[dict],        # [{key, label, region, jobs:[...]}, ...]
    palettes: dict,                    # from config.INDUSTRY_PALETTES
    job_accents: list,                 # from config.JOB_CARD_ACCENTS
    run_id: str,
    cache_ttl: int,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html = _TEMPLATE
    html = html.replace("__NOW__",             now)
    html = html.replace("__TTL__",             str(cache_ttl))
    html = html.replace("__RUN_ID__",          run_id)
    html = html.replace("__INDUSTRIES_JSON__", json.dumps(all_industries, ensure_ascii=False))
    html = html.replace("__PALETTES_JSON__",   json.dumps(palettes,       ensure_ascii=False))
    html = html.replace("__JOB_ACCENTS_JSON__",json.dumps(job_accents,    ensure_ascii=False))
    return html


def write_dashboard(
    html: str,
    output_dir: Path,
    run_id: str,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"dashboard_{run_id}.html"
    path = output_dir / filename
    path.write_text(html, encoding="utf-8")

    # Also overwrite a fixed "latest.html" for easy cron bookmark
    latest = output_dir / "dashboard_latest.html"
    latest.write_text(html, encoding="utf-8")

    return path
