"""
config.py
=========
Central configuration: industry registry, colour palettes, and seed data.

To add a new industry:
    1. Add an entry to INDUSTRY_REGISTRY
    2. Optionally add seed data to SEED_DATA for dry-run support
"""

from __future__ import annotations

# ──────────────────────────────────────────────────────────────────────────────
# Pipeline settings
# ──────────────────────────────────────────────────────────────────────────────
CACHE_TTL_HOURS   = 72      # re-fetch after this many hours
TOP_JOBS          = 5       # jobs per industry
TOP_STD_SKILLS    = 5       # standard skills per job
TOP_TECH_SKILLS   = 4       # tech skills per standard skill (3-5 range target)
API_RETRIES       = 3       # Anthropic API retry attempts
MODEL             = "claude-sonnet-4-5"

# ──────────────────────────────────────────────────────────────────────────────
# Colour palettes  (one per industry, HSL-harmonised)
# ──────────────────────────────────────────────────────────────────────────────
INDUSTRY_PALETTES: dict[str, dict] = {
    "transportation": {
        "primary":   "#3B82F6",   # blue
        "secondary": "#93C5FD",
        "accent":    "#1D4ED8",
        "glow":      "rgba(59,130,246,0.25)",
        "emoji":     "🚚",
    },
    "data_ai": {
        "primary":   "#8B5CF6",   # violet
        "secondary": "#C4B5FD",
        "accent":    "#6D28D9",
        "glow":      "rgba(139,92,246,0.25)",
        "emoji":     "🤖",
    },
    "it_cyber": {
        "primary":   "#06B6D4",   # cyan
        "secondary": "#67E8F9",
        "accent":    "#0E7490",
        "glow":      "rgba(6,182,212,0.25)",
        "emoji":     "🔐",
    },
    "healthcare": {
        "primary":   "#EC4899",   # pink
        "secondary": "#F9A8D4",
        "accent":    "#BE185D",
        "glow":      "rgba(236,72,153,0.25)",
        "emoji":     "🏥",
    },
    "manufacturing": {
        "primary":   "#F59E0B",   # amber
        "secondary": "#FCD34D",
        "accent":    "#B45309",
        "glow":      "rgba(245,158,11,0.25)",
        "emoji":     "⚙️",
    },
    "energy": {
        "primary":   "#22C55E",   # green
        "secondary": "#86EFAC",
        "accent":    "#15803D",
        "glow":      "rgba(34,197,94,0.25)",
        "emoji":     "⚡",
    },
}

# Job-card accent colours (cycled within each industry panel)
JOB_CARD_ACCENTS = [
    "#60A5FA", "#34D399", "#FBBF24", "#F472B6", "#A78BFA",
]

# ──────────────────────────────────────────────────────────────────────────────
# Industry registry
# ──────────────────────────────────────────────────────────────────────────────
INDUSTRY_REGISTRY: dict[str, dict] = {
    "transportation": {
        "label":  "Transportation / Logistics / Supply Chain",
        "region": "United States",
        # Seed jobs used for dry-run (overridden by live search)
        "seed_jobs": [
            "Supply Chain Manager",
            "Logistics Coordinator",
            "Truck Driver",
            "Warehouse Operations Manager",
            "Cargo Handler",
        ],
    },
    "data_ai": {
        "label":  "Data / Artificial Intelligence",
        "region": "United States",
        "seed_jobs": [
            "Data Scientist",
            "Machine Learning Engineer",
            "Data Analyst",
            "AI Product Manager",
            "Data Engineer",
        ],
    },
    "it_cyber": {
        "label":  "IT / Cybersecurity",
        "region": "United States",
        "seed_jobs": [
            "Cybersecurity Analyst",
            "Cloud Engineer",
            "Network Administrator",
            "DevOps Engineer",
            "IT Project Manager",
        ],
    },
    "healthcare": {
        "label":  "Healthcare",
        "region": "United States",
        "seed_jobs": [
            "Registered Nurse",
            "Medical & Health Services Manager",
            "Physical Therapist",
            "Medical Coder / Biller",
            "Clinical Data Analyst",
        ],
    },
    "manufacturing": {
        "label":  "Manufacturing",
        "region": "United States",
        "seed_jobs": [
            "Manufacturing Engineer",
            "Quality Control Inspector",
            "CNC Machinist",
            "Industrial Maintenance Technician",
            "Production Supervisor",
        ],
    },
    "energy": {
        "label":  "Energy & Sustainability",
        "region": "United States",
        "seed_jobs": [
            "Renewable Energy Project Manager",
            "Solar Panel Installer",
            "Wind Turbine Technician",
            "Energy Analyst",
            "Petroleum Engineer",
        ],
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# Seed data — full structured records used when no API key is present.
# These reflect research from BLS O*NET, LinkedIn, Indeed, Glassdoor 2024-2025.
# Structure mirrors the JSON the API returns.
# ──────────────────────────────────────────────────────────────────────────────
SEED_DATA: dict[str, dict] = {

    # ── TRANSPORTATION ────────────────────────────────────────────────────────
    "Supply Chain Manager": {
        "job_title": "Supply Chain Manager", "posting_rank": 1,
        "median_salary_usd": "$95,000–$115,000", "employment_growth": "+17% (2024-2034)",
        "standard_skills": [
            {"name": "Verbal Communication",  "mentions": 9, "rank": 1, "tech_skills": [
                {"name": "Microsoft Teams / Slack", "mentions": 8, "rank": 1},
                {"name": "Zoom / Video Conferencing", "mentions": 7, "rank": 2},
                {"name": "SAP Collaboration Tools", "mentions": 6, "rank": 3},
            ]},
            {"name": "Analytical Thinking",   "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Tableau / Power BI", "mentions": 9, "rank": 1},
                {"name": "SQL", "mentions": 8, "rank": 2},
                {"name": "Excel / Google Sheets", "mentions": 9, "rank": 3},
                {"name": "Python (pandas)", "mentions": 6, "rank": 4},
            ]},
            {"name": "Problem Solving",       "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "ERP Systems (SAP/Oracle)", "mentions": 9, "rank": 1},
                {"name": "Simulation Software", "mentions": 5, "rank": 2},
                {"name": "Operations Research Tools", "mentions": 4, "rank": 3},
            ]},
            {"name": "Negotiation",           "mentions": 7, "rank": 4, "tech_skills": [
                {"name": "Contract Mgmt Software", "mentions": 6, "rank": 1},
                {"name": "Ariba / Coupa (Procurement)", "mentions": 7, "rank": 2},
                {"name": "Salesforce CRM", "mentions": 5, "rank": 3},
            ]},
            {"name": "Leadership",            "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Jira / Asana (Project Mgmt)", "mentions": 7, "rank": 1},
                {"name": "Microsoft Project", "mentions": 6, "rank": 2},
                {"name": "Workday HCM", "mentions": 5, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/business-and-financial/logisticians.htm",
                    "https://parakeetrisk.com/blog/supply-chain-careers-in-2025"]
    },
    "Logistics Coordinator": {
        "job_title": "Logistics Coordinator", "posting_rank": 2,
        "median_salary_usd": "$48,000–$65,000", "employment_growth": "+13% (2024-2034)",
        "standard_skills": [
            {"name": "Organizational Skills", "mentions": 9, "rank": 1, "tech_skills": [
                {"name": "WMS (Warehouse Mgmt Systems)", "mentions": 9, "rank": 1},
                {"name": "TMS (Transportation Mgmt)", "mentions": 8, "rank": 2},
                {"name": "Excel / Google Sheets", "mentions": 9, "rank": 3},
            ]},
            {"name": "Attention to Detail",   "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Barcode / RFID Systems", "mentions": 8, "rank": 1},
                {"name": "EDI (Electronic Data Interchange)", "mentions": 7, "rank": 2},
                {"name": "SAP Logistics", "mentions": 7, "rank": 3},
            ]},
            {"name": "Communication",         "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "Slack / Teams", "mentions": 8, "rank": 1},
                {"name": "Carrier Portals (FedEx, UPS)", "mentions": 8, "rank": 2},
                {"name": "Email Automation Tools", "mentions": 6, "rank": 3},
            ]},
            {"name": "Time Management",       "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Route Optimization Software", "mentions": 7, "rank": 1},
                {"name": "Fleet Tracking (Samsara/Verizon)", "mentions": 7, "rank": 2},
                {"name": "Scheduling Software", "mentions": 6, "rank": 3},
            ]},
            {"name": "Problem Solving",       "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Power BI / Tableau", "mentions": 6, "rank": 1},
                {"name": "SQL (basic)", "mentions": 5, "rank": 2},
                {"name": "Freight Audit Software", "mentions": 5, "rank": 3},
            ]},
        ],
        "sources": ["https://www.indeed.com/career-advice/careers/what-does-a-logistics-coordinator-do"]
    },
    "Truck Driver": {
        "job_title": "Truck Driver", "posting_rank": 3,
        "median_salary_usd": "$50,000–$80,000", "employment_growth": "+4% (2024-2034)",
        "standard_skills": [
            {"name": "Safe & Defensive Driving", "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "ELD (Electronic Logging Device)", "mentions": 10, "rank": 1},
                {"name": "GPS / Route Navigation Apps", "mentions": 10, "rank": 2},
                {"name": "ADAS (Collision Avoidance)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Time Management",       "mentions": 8, "rank": 2, "tech_skills": [
                {"name": "Fleet Mgmt Software (Samsara)", "mentions": 8, "rank": 1},
                {"name": "Load-Tracking Mobile Apps", "mentions": 7, "rank": 2},
                {"name": "HOS Compliance Tools", "mentions": 8, "rank": 3},
            ]},
            {"name": "Physical Stamina",      "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "Telematics / OBD Systems", "mentions": 7, "rank": 1},
                {"name": "In-Cab Communications", "mentions": 6, "rank": 2},
                {"name": "Pre-Trip Inspection Apps", "mentions": 6, "rank": 3},
            ]},
            {"name": "Adaptability",          "mentions": 7, "rank": 4, "tech_skills": [
                {"name": "Weather & Traffic Apps", "mentions": 8, "rank": 1},
                {"name": "Load Board Platforms (DAT)", "mentions": 7, "rank": 2},
                {"name": "Digital Freight Matching", "mentions": 6, "rank": 3},
            ]},
            {"name": "Regulatory Knowledge",  "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "FMCSA Compliance Software", "mentions": 8, "rank": 1},
                {"name": "Hazmat Documentation Tools", "mentions": 6, "rank": 2},
                {"name": "CDL Training Platforms", "mentions": 5, "rank": 3},
            ]},
        ],
        "sources": ["https://huntr.co/resume-skills/truck-driver"]
    },
    "Warehouse Operations Manager": {
        "job_title": "Warehouse Operations Manager", "posting_rank": 4,
        "median_salary_usd": "$65,000–$90,000", "employment_growth": "+8% (2024-2034)",
        "standard_skills": [
            {"name": "Leadership & Team Mgmt", "mentions": 9, "rank": 1, "tech_skills": [
                {"name": "WMS (Manhattan/HighJump)", "mentions": 9, "rank": 1},
                {"name": "Workday / SAP HCM", "mentions": 7, "rank": 2},
                {"name": "KPI Dashboards (Power BI)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Process Optimization",  "mentions": 8, "rank": 2, "tech_skills": [
                {"name": "Lean / Six Sigma Tools", "mentions": 8, "rank": 1},
                {"name": "Warehouse Automation (robotics)", "mentions": 7, "rank": 2},
                {"name": "RFID / IoT Sensors", "mentions": 7, "rank": 3},
                {"name": "AutoStore / Conveyor Systems", "mentions": 5, "rank": 4},
            ]},
            {"name": "Inventory Management",  "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "ERP Inventory Module", "mentions": 9, "rank": 1},
                {"name": "Cycle-Count Software", "mentions": 7, "rank": 2},
                {"name": "Demand Forecasting Tools", "mentions": 6, "rank": 3},
            ]},
            {"name": "Safety Compliance",     "mentions": 7, "rank": 4, "tech_skills": [
                {"name": "OSHA Compliance Platforms", "mentions": 8, "rank": 1},
                {"name": "Incident Reporting Software", "mentions": 7, "rank": 2},
                {"name": "Forklift Mgmt Systems", "mentions": 6, "rank": 3},
            ]},
            {"name": "Communication",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Slack / Microsoft Teams", "mentions": 8, "rank": 1},
                {"name": "Shift Scheduling Software", "mentions": 7, "rank": 2},
                {"name": "Voice-Directed Picking", "mentions": 5, "rank": 3},
            ]},
        ],
        "sources": ["https://www.glassdoor.com/Career/warehouse-operations-manager-career_KO0,28.htm"]
    },
    "Cargo Handler": {
        "job_title": "Cargo Handler", "posting_rank": 5,
        "median_salary_usd": "$36,000–$52,000", "employment_growth": "+6% (2024-2034)",
        "standard_skills": [
            {"name": "Physical Stamina",      "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "Forklift / Pallet Jack", "mentions": 10, "rank": 1},
                {"name": "Material Handling Equipment", "mentions": 9, "rank": 2},
                {"name": "PPE & Safety Systems", "mentions": 8, "rank": 3},
            ]},
            {"name": "Attention to Detail",   "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Barcode / RFID Scanners", "mentions": 9, "rank": 1},
                {"name": "Cargo Documentation Software", "mentions": 7, "rank": 2},
                {"name": "Inventory Mgmt Systems", "mentions": 7, "rank": 3},
            ]},
            {"name": "Teamwork",              "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "WMS (basic)", "mentions": 8, "rank": 1},
                {"name": "Radio / Headset Comms", "mentions": 7, "rank": 2},
                {"name": "Shift-Coordination Apps", "mentions": 5, "rank": 3},
            ]},
            {"name": "Mathematical Reasoning","mentions": 7, "rank": 4, "tech_skills": [
                {"name": "Weight & Balance Software", "mentions": 7, "rank": 1},
                {"name": "Load-Planning Tools", "mentions": 6, "rank": 2},
                {"name": "Basic Computer / Data Entry", "mentions": 7, "rank": 3},
            ]},
            {"name": "Safety Awareness",      "mentions": 8, "rank": 5, "tech_skills": [
                {"name": "OSHA / HazMat Certification", "mentions": 8, "rank": 1},
                {"name": "Fire Safety Systems", "mentions": 6, "rank": 2},
                {"name": "Incident Reporting Tools", "mentions": 5, "rank": 3},
            ]},
        ],
        "sources": ["https://www.zippia.com/cargo-handler-jobs/job-description/"]
    },

    # ── DATA / AI ────────────────────────────────────────────────────────────
    "Data Scientist": {
        "job_title": "Data Scientist", "posting_rank": 1,
        "median_salary_usd": "$105,000–$145,000", "employment_growth": "+35% (2024-2034)",
        "standard_skills": [
            {"name": "Statistical Analysis",  "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "Python (NumPy/SciPy/statsmodels)", "mentions": 10, "rank": 1},
                {"name": "R", "mentions": 8, "rank": 2},
                {"name": "SQL", "mentions": 9, "rank": 3},
                {"name": "Jupyter Notebooks", "mentions": 8, "rank": 4},
            ]},
            {"name": "Machine Learning",      "mentions": 10, "rank": 2, "tech_skills": [
                {"name": "Scikit-learn / XGBoost", "mentions": 10, "rank": 1},
                {"name": "TensorFlow / PyTorch", "mentions": 9, "rank": 2},
                {"name": "MLflow / Weights & Biases", "mentions": 7, "rank": 3},
                {"name": "Hugging Face Transformers", "mentions": 7, "rank": 4},
            ]},
            {"name": "Data Wrangling",        "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "pandas / polars", "mentions": 10, "rank": 1},
                {"name": "Apache Spark / PySpark", "mentions": 8, "rank": 2},
                {"name": "dbt (data build tool)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Data Visualization",    "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Tableau / Power BI", "mentions": 9, "rank": 1},
                {"name": "Matplotlib / Seaborn / Plotly", "mentions": 9, "rank": 2},
                {"name": "Looker / Metabase", "mentions": 6, "rank": 3},
            ]},
            {"name": "Critical Thinking",     "mentions": 8, "rank": 5, "tech_skills": [
                {"name": "A/B Testing Frameworks", "mentions": 7, "rank": 1},
                {"name": "Causal Inference Tools", "mentions": 6, "rank": 2},
                {"name": "Experiment Design Software", "mentions": 5, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/math/data-scientists.htm"]
    },
    "Machine Learning Engineer": {
        "job_title": "Machine Learning Engineer", "posting_rank": 2,
        "median_salary_usd": "$120,000–$165,000", "employment_growth": "+40% (2024-2034)",
        "standard_skills": [
            {"name": "Software Engineering",  "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "Python / C++", "mentions": 10, "rank": 1},
                {"name": "Git / GitHub Actions", "mentions": 9, "rank": 2},
                {"name": "Docker / Kubernetes", "mentions": 9, "rank": 3},
                {"name": "FastAPI / gRPC", "mentions": 7, "rank": 4},
            ]},
            {"name": "Deep Learning",         "mentions": 10, "rank": 2, "tech_skills": [
                {"name": "PyTorch / TensorFlow", "mentions": 10, "rank": 1},
                {"name": "CUDA / GPU Programming", "mentions": 8, "rank": 2},
                {"name": "ONNX / TensorRT", "mentions": 7, "rank": 3},
            ]},
            {"name": "MLOps & Deployment",    "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "MLflow / Kubeflow", "mentions": 9, "rank": 1},
                {"name": "AWS SageMaker / GCP Vertex AI", "mentions": 9, "rank": 2},
                {"name": "Airflow / Prefect", "mentions": 7, "rank": 3},
                {"name": "Prometheus / Grafana", "mentions": 6, "rank": 4},
            ]},
            {"name": "Problem Decomposition", "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Feature Stores (Feast/Tecton)", "mentions": 7, "rank": 1},
                {"name": "Experiment Tracking Tools", "mentions": 7, "rank": 2},
                {"name": "Hyperparameter Optimisation", "mentions": 6, "rank": 3},
            ]},
            {"name": "Research Literacy",     "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "arXiv / Papers With Code", "mentions": 7, "rank": 1},
                {"name": "Hugging Face Hub", "mentions": 8, "rank": 2},
                {"name": "LangChain / LlamaIndex", "mentions": 7, "rank": 3},
            ]},
        ],
        "sources": ["https://www.linkedin.com/jobs/machine-learning-engineer-jobs/"]
    },
    "Data Analyst": {
        "job_title": "Data Analyst", "posting_rank": 3,
        "median_salary_usd": "$65,000–$95,000", "employment_growth": "+23% (2024-2034)",
        "standard_skills": [
            {"name": "Analytical Thinking",   "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "SQL", "mentions": 10, "rank": 1},
                {"name": "Excel / Google Sheets", "mentions": 10, "rank": 2},
                {"name": "Python (pandas)", "mentions": 8, "rank": 3},
            ]},
            {"name": "Data Visualization",    "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Tableau / Power BI", "mentions": 10, "rank": 1},
                {"name": "Looker / Metabase", "mentions": 7, "rank": 2},
                {"name": "Matplotlib / Plotly", "mentions": 7, "rank": 3},
            ]},
            {"name": "Communication",         "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "PowerPoint / Google Slides", "mentions": 9, "rank": 1},
                {"name": "Confluence / Notion", "mentions": 7, "rank": 2},
                {"name": "Storytelling with Data", "mentions": 6, "rank": 3},
            ]},
            {"name": "Statistical Reasoning", "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "R / Python (statsmodels)", "mentions": 7, "rank": 1},
                {"name": "A/B Testing Tools", "mentions": 7, "rank": 2},
                {"name": "Google Analytics / Adobe Analytics", "mentions": 7, "rank": 3},
            ]},
            {"name": "Attention to Detail",   "mentions": 8, "rank": 5, "tech_skills": [
                {"name": "dbt / Great Expectations", "mentions": 6, "rank": 1},
                {"name": "Data Quality Tools", "mentions": 6, "rank": 2},
                {"name": "Databricks / Snowflake", "mentions": 7, "rank": 3},
            ]},
        ],
        "sources": ["https://www.glassdoor.com/Career/data-analyst-career_KO0,12.htm"]
    },
    "AI Product Manager": {
        "job_title": "AI Product Manager", "posting_rank": 4,
        "median_salary_usd": "$130,000–$175,000", "employment_growth": "+19% (2024-2034)",
        "standard_skills": [
            {"name": "Product Strategy",      "mentions": 9, "rank": 1, "tech_skills": [
                {"name": "Jira / Linear (Roadmapping)", "mentions": 9, "rank": 1},
                {"name": "Productboard / Aha!", "mentions": 7, "rank": 2},
                {"name": "Amplitude / Mixpanel", "mentions": 7, "rank": 3},
            ]},
            {"name": "AI/ML Literacy",        "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "OpenAI / Anthropic APIs", "mentions": 9, "rank": 1},
                {"name": "Hugging Face Models", "mentions": 7, "rank": 2},
                {"name": "LLM Evaluation Tools", "mentions": 7, "rank": 3},
                {"name": "Prompt Engineering", "mentions": 8, "rank": 4},
            ]},
            {"name": "Stakeholder Communication", "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "Figma / Miro (Collaboration)", "mentions": 8, "rank": 1},
                {"name": "Confluence / Notion", "mentions": 7, "rank": 2},
                {"name": "SQL (ad-hoc analysis)", "mentions": 6, "rank": 3},
            ]},
            {"name": "Data-Driven Decision Making", "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Tableau / Looker", "mentions": 8, "rank": 1},
                {"name": "A/B Testing Platforms", "mentions": 7, "rank": 2},
                {"name": "Python (basic scripting)", "mentions": 6, "rank": 3},
            ]},
            {"name": "Agile / Scrum",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Jira / GitHub Projects", "mentions": 9, "rank": 1},
                {"name": "Notion / Confluence", "mentions": 7, "rank": 2},
                {"name": "CI/CD Awareness (GitHub Actions)", "mentions": 5, "rank": 3},
            ]},
        ],
        "sources": ["https://www.linkedin.com/jobs/ai-product-manager-jobs/"]
    },
    "Data Engineer": {
        "job_title": "Data Engineer", "posting_rank": 5,
        "median_salary_usd": "$100,000–$140,000", "employment_growth": "+28% (2024-2034)",
        "standard_skills": [
            {"name": "Data Modelling",        "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "SQL / dbt", "mentions": 10, "rank": 1},
                {"name": "Snowflake / BigQuery / Redshift", "mentions": 9, "rank": 2},
                {"name": "Apache Iceberg / Delta Lake", "mentions": 7, "rank": 3},
            ]},
            {"name": "Pipeline Development",  "mentions": 10, "rank": 2, "tech_skills": [
                {"name": "Apache Airflow / Prefect", "mentions": 9, "rank": 1},
                {"name": "Apache Spark / Flink", "mentions": 8, "rank": 2},
                {"name": "Kafka / Kinesis", "mentions": 8, "rank": 3},
                {"name": "Python", "mentions": 10, "rank": 4},
            ]},
            {"name": "Cloud Infrastructure",  "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "AWS / GCP / Azure", "mentions": 10, "rank": 1},
                {"name": "Terraform / IaC", "mentions": 8, "rank": 2},
                {"name": "Docker / Kubernetes", "mentions": 8, "rank": 3},
            ]},
            {"name": "Problem Solving",       "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Great Expectations / Soda", "mentions": 7, "rank": 1},
                {"name": "Data Observability (Monte Carlo)", "mentions": 6, "rank": 2},
                {"name": "OpenLineage / Marquez", "mentions": 5, "rank": 3},
            ]},
            {"name": "Collaboration",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Git / GitHub / GitLab", "mentions": 9, "rank": 1},
                {"name": "Jira / Notion", "mentions": 7, "rank": 2},
                {"name": "Slack / Teams", "mentions": 8, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/math/data-scientists.htm"]
    },

    # ── IT / CYBERSECURITY ────────────────────────────────────────────────────
    "Cybersecurity Analyst": {
        "job_title": "Cybersecurity Analyst", "posting_rank": 1,
        "median_salary_usd": "$95,000–$130,000", "employment_growth": "+33% (2024-2034)",
        "standard_skills": [
            {"name": "Threat Analysis",       "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "SIEM (Splunk / Microsoft Sentinel)", "mentions": 10, "rank": 1},
                {"name": "CrowdStrike / SentinelOne EDR", "mentions": 9, "rank": 2},
                {"name": "MITRE ATT&CK Framework", "mentions": 8, "rank": 3},
                {"name": "Threat Intelligence Platforms", "mentions": 7, "rank": 4},
            ]},
            {"name": "Incident Response",     "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "SOAR Platforms (Palo Alto XSOAR)", "mentions": 8, "rank": 1},
                {"name": "Forensic Tools (Volatility/Autopsy)", "mentions": 7, "rank": 2},
                {"name": "Wireshark / tcpdump", "mentions": 8, "rank": 3},
            ]},
            {"name": "Risk Assessment",       "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "Nessus / Qualys (Vulnerability Scanning)", "mentions": 9, "rank": 1},
                {"name": "GRC Platforms (ServiceNow)", "mentions": 7, "rank": 2},
                {"name": "NIST / ISO 27001 Frameworks", "mentions": 8, "rank": 3},
            ]},
            {"name": "Critical Thinking",     "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Penetration Testing (Metasploit/Burp Suite)", "mentions": 7, "rank": 1},
                {"name": "Python / Bash Scripting", "mentions": 8, "rank": 2},
                {"name": "Threat Hunting Tools", "mentions": 6, "rank": 3},
            ]},
            {"name": "Communication",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Security Report Writing Tools", "mentions": 6, "rank": 1},
                {"name": "Jira / ServiceNow (Ticketing)", "mentions": 7, "rank": 2},
                {"name": "Confluence / SharePoint", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm"]
    },
    "Cloud Engineer": {
        "job_title": "Cloud Engineer", "posting_rank": 2,
        "median_salary_usd": "$110,000–$155,000", "employment_growth": "+25% (2024-2034)",
        "standard_skills": [
            {"name": "Cloud Architecture",    "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "AWS / GCP / Azure", "mentions": 10, "rank": 1},
                {"name": "Terraform / Pulumi", "mentions": 9, "rank": 2},
                {"name": "CloudFormation / ARM Templates", "mentions": 7, "rank": 3},
            ]},
            {"name": "Automation & Scripting","mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Python / Bash / PowerShell", "mentions": 10, "rank": 1},
                {"name": "Ansible / Chef / Puppet", "mentions": 8, "rank": 2},
                {"name": "GitHub Actions / Jenkins", "mentions": 8, "rank": 3},
            ]},
            {"name": "Containerization",      "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "Docker", "mentions": 10, "rank": 1},
                {"name": "Kubernetes / EKS / GKE", "mentions": 10, "rank": 2},
                {"name": "Helm Charts", "mentions": 8, "rank": 3},
                {"name": "Istio / Service Mesh", "mentions": 6, "rank": 4},
            ]},
            {"name": "Problem Solving",       "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Prometheus / Grafana", "mentions": 8, "rank": 1},
                {"name": "Datadog / New Relic", "mentions": 7, "rank": 2},
                {"name": "PagerDuty / OpsGenie", "mentions": 6, "rank": 3},
            ]},
            {"name": "Security Awareness",    "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "IAM / Zero Trust (Okta)", "mentions": 8, "rank": 1},
                {"name": "Cloud Security Posture (Prisma Cloud)", "mentions": 7, "rank": 2},
                {"name": "Secrets Mgmt (Vault)", "mentions": 7, "rank": 3},
            ]},
        ],
        "sources": ["https://www.glassdoor.com/Career/cloud-engineer-career_KO0,14.htm"]
    },
    "Network Administrator": {
        "job_title": "Network Administrator", "posting_rank": 3,
        "median_salary_usd": "$65,000–$95,000", "employment_growth": "+2% (2024-2034)",
        "standard_skills": [
            {"name": "Network Configuration",  "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "Cisco IOS / NX-OS", "mentions": 10, "rank": 1},
                {"name": "Juniper Junos", "mentions": 7, "rank": 2},
                {"name": "SD-WAN (Cisco Viptela / VMware)", "mentions": 8, "rank": 3},
            ]},
            {"name": "Troubleshooting",       "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Wireshark / SolarWinds", "mentions": 9, "rank": 1},
                {"name": "PRTG / Nagios (Monitoring)", "mentions": 8, "rank": 2},
                {"name": "Traceroute / Ping Tools", "mentions": 7, "rank": 3},
            ]},
            {"name": "Security Fundamentals", "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "Firewalls (Palo Alto / Fortinet)", "mentions": 9, "rank": 1},
                {"name": "VPN / Zero Trust", "mentions": 8, "rank": 2},
                {"name": "RADIUS / TACACS+", "mentions": 6, "rank": 3},
            ]},
            {"name": "Documentation",         "mentions": 7, "rank": 4, "tech_skills": [
                {"name": "NetBox / IP Address Mgmt", "mentions": 7, "rank": 1},
                {"name": "Confluence / SharePoint", "mentions": 7, "rank": 2},
                {"name": "Visio / Lucidchart (Diagrams)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Collaboration",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "ServiceNow / Jira (ITSM)", "mentions": 8, "rank": 1},
                {"name": "Slack / Teams", "mentions": 8, "rank": 2},
                {"name": "Python / Ansible (NetDevOps)", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/computer-and-information-technology/network-and-computer-systems-administrators.htm"]
    },
    "DevOps Engineer": {
        "job_title": "DevOps Engineer", "posting_rank": 4,
        "median_salary_usd": "$115,000–$155,000", "employment_growth": "+21% (2024-2034)",
        "standard_skills": [
            {"name": "CI/CD Pipeline Design", "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "GitHub Actions / GitLab CI", "mentions": 10, "rank": 1},
                {"name": "Jenkins / CircleCI", "mentions": 8, "rank": 2},
                {"name": "ArgoCD / Flux (GitOps)", "mentions": 8, "rank": 3},
                {"name": "Tekton Pipelines", "mentions": 5, "rank": 4},
            ]},
            {"name": "Infrastructure as Code","mentions": 10, "rank": 2, "tech_skills": [
                {"name": "Terraform", "mentions": 10, "rank": 1},
                {"name": "Ansible / Chef", "mentions": 8, "rank": 2},
                {"name": "AWS CDK / Pulumi", "mentions": 7, "rank": 3},
            ]},
            {"name": "Systems Thinking",      "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "Prometheus / Grafana", "mentions": 9, "rank": 1},
                {"name": "Datadog / Dynatrace", "mentions": 8, "rank": 2},
                {"name": "OpenTelemetry", "mentions": 7, "rank": 3},
            ]},
            {"name": "Collaboration",         "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Jira / Linear", "mentions": 9, "rank": 1},
                {"name": "Confluence / Notion", "mentions": 7, "rank": 2},
                {"name": "Slack / Teams", "mentions": 8, "rank": 3},
            ]},
            {"name": "Security Awareness",    "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Vault / AWS Secrets Manager", "mentions": 8, "rank": 1},
                {"name": "Snyk / Trivy (Container Scanning)", "mentions": 7, "rank": 2},
                {"name": "SAST / DAST Tools", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.linkedin.com/jobs/devops-engineer-jobs/"]
    },
    "IT Project Manager": {
        "job_title": "IT Project Manager", "posting_rank": 5,
        "median_salary_usd": "$95,000–$130,000", "employment_growth": "+7% (2024-2034)",
        "standard_skills": [
            {"name": "Project Planning",      "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "MS Project / Smartsheet", "mentions": 9, "rank": 1},
                {"name": "Jira / Asana", "mentions": 9, "rank": 2},
                {"name": "Monday.com", "mentions": 7, "rank": 3},
            ]},
            {"name": "Stakeholder Management","mentions": 9, "rank": 2, "tech_skills": [
                {"name": "PowerPoint / Google Slides", "mentions": 9, "rank": 1},
                {"name": "Confluence / SharePoint", "mentions": 8, "rank": 2},
                {"name": "ServiceNow (ITSM)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Risk Management",       "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "GRC Platforms (Archer)", "mentions": 7, "rank": 1},
                {"name": "Risk Register Tools", "mentions": 7, "rank": 2},
                {"name": "Excel / Google Sheets", "mentions": 8, "rank": 3},
            ]},
            {"name": "Agile / Scrum",         "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Jira (Scrum/Kanban)", "mentions": 10, "rank": 1},
                {"name": "Miro / Mural", "mentions": 7, "rank": 2},
                {"name": "Azure DevOps", "mentions": 7, "rank": 3},
            ]},
            {"name": "Communication",         "mentions": 8, "rank": 5, "tech_skills": [
                {"name": "Slack / Teams", "mentions": 9, "rank": 1},
                {"name": "Zoom / Webex", "mentions": 8, "rank": 2},
                {"name": "Notion / Confluence", "mentions": 7, "rank": 3},
            ]},
        ],
        "sources": ["https://www.pmi.org/learning/library/project-management-career-outlook-9590"]
    },

    # ── HEALTHCARE ────────────────────────────────────────────────────────────
    "Registered Nurse": {
        "job_title": "Registered Nurse", "posting_rank": 1,
        "median_salary_usd": "$75,000–$95,000", "employment_growth": "+6% (2024-2034)",
        "standard_skills": [
            {"name": "Patient Assessment",    "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "EHR (Epic / Cerner)", "mentions": 10, "rank": 1},
                {"name": "Vital Signs Monitors", "mentions": 9, "rank": 2},
                {"name": "Telemetry / ECG Systems", "mentions": 8, "rank": 3},
            ]},
            {"name": "Clinical Judgment",     "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Clinical Decision Support (CDS)", "mentions": 8, "rank": 1},
                {"name": "CPOE (Computerised Physician Order Entry)", "mentions": 8, "rank": 2},
                {"name": "UpToDate / Clinical Evidence Tools", "mentions": 7, "rank": 3},
            ]},
            {"name": "Communication",         "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "SBAR Communication Tools", "mentions": 8, "rank": 1},
                {"name": "Secure Messaging (TigerConnect)", "mentions": 7, "rank": 2},
                {"name": "Patient Portal Software", "mentions": 7, "rank": 3},
            ]},
            {"name": "Empathy & Patient Care","mentions": 9, "rank": 4, "tech_skills": [
                {"name": "Patient Satisfaction Platforms (Press Ganey)", "mentions": 7, "rank": 1},
                {"name": "Care Coordination Software", "mentions": 6, "rank": 2},
                {"name": "Telehealth Platforms (Teladoc)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Critical Thinking",     "mentions": 8, "rank": 5, "tech_skills": [
                {"name": "Medication Administration Systems (Pyxis)", "mentions": 9, "rank": 1},
                {"name": "IV Pump / Smart Infusion Tech", "mentions": 8, "rank": 2},
                {"name": "Barcode Medication Verification", "mentions": 7, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/healthcare/registered-nurses.htm"]
    },
    "Medical & Health Services Manager": {
        "job_title": "Medical & Health Services Manager", "posting_rank": 2,
        "median_salary_usd": "$100,000–$135,000", "employment_growth": "+28% (2024-2034)",
        "standard_skills": [
            {"name": "Healthcare Operations",  "mentions": 9, "rank": 1, "tech_skills": [
                {"name": "EHR Systems (Epic/Cerner)", "mentions": 9, "rank": 1},
                {"name": "Healthcare Analytics (Tableau)", "mentions": 8, "rank": 2},
                {"name": "RCM Software (Optum/Waystar)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Leadership & Strategy",  "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Workday / Oracle HCM", "mentions": 8, "rank": 1},
                {"name": "Microsoft Project", "mentions": 7, "rank": 2},
                {"name": "Power BI / Tableau", "mentions": 8, "rank": 3},
            ]},
            {"name": "Regulatory Compliance", "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "HIPAA Compliance Software", "mentions": 9, "rank": 1},
                {"name": "Joint Commission Tracking Tools", "mentions": 7, "rank": 2},
                {"name": "GRC Platforms", "mentions": 6, "rank": 3},
            ]},
            {"name": "Financial Acumen",       "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Budgeting Software (Axiom)", "mentions": 7, "rank": 1},
                {"name": "Excel / Google Sheets", "mentions": 9, "rank": 2},
                {"name": "Cost Accounting Tools", "mentions": 6, "rank": 3},
            ]},
            {"name": "Communication",          "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Slack / Teams", "mentions": 8, "rank": 1},
                {"name": "Zoom / Webex", "mentions": 7, "rank": 2},
                {"name": "SharePoint / Confluence", "mentions": 7, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/management/medical-and-health-services-managers.htm"]
    },
    "Physical Therapist": {
        "job_title": "Physical Therapist", "posting_rank": 3,
        "median_salary_usd": "$80,000–$100,000", "employment_growth": "+17% (2024-2034)",
        "standard_skills": [
            {"name": "Clinical Assessment",   "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "EHR (WebPT / Epic)", "mentions": 10, "rank": 1},
                {"name": "Outcome Measurement Tools (FOTO)", "mentions": 8, "rank": 2},
                {"name": "Motion Analysis Software", "mentions": 7, "rank": 3},
            ]},
            {"name": "Treatment Planning",    "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Rehab Software (Keet/Clinicient)", "mentions": 8, "rank": 1},
                {"name": "Telehealth Platforms", "mentions": 7, "rank": 2},
                {"name": "Evidence-Based Practice Databases", "mentions": 7, "rank": 3},
            ]},
            {"name": "Patient Education",     "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "Patient Portal Apps", "mentions": 8, "rank": 1},
                {"name": "Digital Exercise Prescription (HEP2go)", "mentions": 7, "rank": 2},
                {"name": "Video Communication Tools", "mentions": 7, "rank": 3},
            ]},
            {"name": "Empathy",               "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Patient Satisfaction Surveys (Press Ganey)", "mentions": 7, "rank": 1},
                {"name": "Care Coordination Software", "mentions": 6, "rank": 2},
                {"name": "Wearable Rehabilitation Devices", "mentions": 6, "rank": 3},
            ]},
            {"name": "Documentation",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "WebPT / Clinicient (EMR)", "mentions": 9, "rank": 1},
                {"name": "Medical Billing Software", "mentions": 7, "rank": 2},
                {"name": "ICD-10 Coding Tools", "mentions": 7, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/healthcare/physical-therapists.htm"]
    },
    "Medical Coder / Biller": {
        "job_title": "Medical Coder / Biller", "posting_rank": 4,
        "median_salary_usd": "$42,000–$62,000", "employment_growth": "+9% (2024-2034)",
        "standard_skills": [
            {"name": "Medical Coding Accuracy","mentions": 10, "rank": 1, "tech_skills": [
                {"name": "ICD-10 / CPT Coding Software", "mentions": 10, "rank": 1},
                {"name": "Encoder Pro / TruCode", "mentions": 9, "rank": 2},
                {"name": "3M HIS Coding Tools", "mentions": 8, "rank": 3},
            ]},
            {"name": "Attention to Detail",   "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "EHR Systems (Epic/Cerner)", "mentions": 9, "rank": 1},
                {"name": "Claims Management Software", "mentions": 8, "rank": 2},
                {"name": "Audit Tools (RAC Tracker)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Regulatory Knowledge",  "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "HIPAA Compliance Platforms", "mentions": 9, "rank": 1},
                {"name": "CMS Guidelines Tools", "mentions": 8, "rank": 2},
                {"name": "Denial Management Software", "mentions": 7, "rank": 3},
            ]},
            {"name": "Analytical Thinking",   "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Revenue Cycle Analytics (Tableau)", "mentions": 7, "rank": 1},
                {"name": "Excel / Google Sheets", "mentions": 9, "rank": 2},
                {"name": "Optum / Waystar RCM", "mentions": 7, "rank": 3},
            ]},
            {"name": "Communication",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Secure Email / Messaging (TigerConnect)", "mentions": 7, "rank": 1},
                {"name": "Practice Mgmt Software (AdvancedMD)", "mentions": 7, "rank": 2},
                {"name": "Patient Communication Portals", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.aapc.com/resources/"]
    },
    "Clinical Data Analyst": {
        "job_title": "Clinical Data Analyst", "posting_rank": 5,
        "median_salary_usd": "$70,000–$100,000", "employment_growth": "+22% (2024-2034)",
        "standard_skills": [
            {"name": "Data Analysis",          "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "SQL", "mentions": 10, "rank": 1},
                {"name": "Python / R", "mentions": 8, "rank": 2},
                {"name": "SAS / SPSS", "mentions": 7, "rank": 3},
            ]},
            {"name": "Healthcare Domain Knowledge", "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Epic/Cerner EHR Analytics", "mentions": 9, "rank": 1},
                {"name": "HL7 / FHIR Standards", "mentions": 8, "rank": 2},
                {"name": "ICD-10 / SNOMED Terminology", "mentions": 7, "rank": 3},
            ]},
            {"name": "Data Visualization",    "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "Tableau / Power BI", "mentions": 9, "rank": 1},
                {"name": "Qlik / MicroStrategy", "mentions": 6, "rank": 2},
                {"name": "R (ggplot2) / Plotly", "mentions": 7, "rank": 3},
            ]},
            {"name": "Critical Thinking",     "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "REDCap (Clinical Data Capture)", "mentions": 8, "rank": 1},
                {"name": "Statistical Methods (ANOVA, regression)", "mentions": 7, "rank": 2},
                {"name": "Clinical Trial Software (Medidata)", "mentions": 6, "rank": 3},
            ]},
            {"name": "Communication",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "PowerPoint / Google Slides", "mentions": 8, "rank": 1},
                {"name": "Confluence / SharePoint", "mentions": 7, "rank": 2},
                {"name": "Slack / Teams", "mentions": 7, "rank": 3},
            ]},
        ],
        "sources": ["https://www.glassdoor.com/Career/clinical-data-analyst-career_KO0,21.htm"]
    },

    # ── MANUFACTURING ────────────────────────────────────────────────────────
    "Manufacturing Engineer": {
        "job_title": "Manufacturing Engineer", "posting_rank": 1,
        "median_salary_usd": "$80,000–$110,000", "employment_growth": "+10% (2024-2034)",
        "standard_skills": [
            {"name": "Process Engineering",   "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "CAD (SolidWorks / AutoCAD)", "mentions": 10, "rank": 1},
                {"name": "Simulation Software (Arena)", "mentions": 8, "rank": 2},
                {"name": "PLM Systems (Siemens Teamcenter)", "mentions": 7, "rank": 3},
                {"name": "DFMEA / PFMEA Tools", "mentions": 7, "rank": 4},
            ]},
            {"name": "Lean / Six Sigma",       "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Minitab / JMP (Statistical Process Control)", "mentions": 9, "rank": 1},
                {"name": "VSM Software (iGrafx)", "mentions": 7, "rank": 2},
                {"name": "Kaizen / 5S Digital Tools", "mentions": 6, "rank": 3},
            ]},
            {"name": "Problem Solving",        "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "Root Cause Analysis Tools (8D, Fishbone)", "mentions": 9, "rank": 1},
                {"name": "SAP Manufacturing", "mentions": 8, "rank": 2},
                {"name": "MES (Manufacturing Execution Systems)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Technical Communication","mentions": 7, "rank": 4, "tech_skills": [
                {"name": "AutoCAD / Visio (Technical Drawing)", "mentions": 8, "rank": 1},
                {"name": "Confluence / SharePoint", "mentions": 7, "rank": 2},
                {"name": "Microsoft Office Suite", "mentions": 8, "rank": 3},
            ]},
            {"name": "Continuous Improvement", "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "ERP (SAP / Oracle)", "mentions": 9, "rank": 1},
                {"name": "IoT / Industry 4.0 Platforms", "mentions": 7, "rank": 2},
                {"name": "Digital Twin Software", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/architecture-and-engineering/industrial-engineers.htm"]
    },
    "Quality Control Inspector": {
        "job_title": "Quality Control Inspector", "posting_rank": 2,
        "median_salary_usd": "$42,000–$62,000", "employment_growth": "+4% (2024-2034)",
        "standard_skills": [
            {"name": "Attention to Detail",    "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "CMM / Metrology Equipment", "mentions": 9, "rank": 1},
                {"name": "Statistical Process Control (SPC) Software", "mentions": 8, "rank": 2},
                {"name": "Vision Inspection Systems", "mentions": 7, "rank": 3},
            ]},
            {"name": "Quality Standards Knowledge","mentions": 9, "rank": 2, "tech_skills": [
                {"name": "ISO 9001 / IATF 16949 Compliance Tools", "mentions": 9, "rank": 1},
                {"name": "QMS Software (ETQ/MasterControl)", "mentions": 8, "rank": 2},
                {"name": "CAPA Management Systems", "mentions": 7, "rank": 3},
            ]},
            {"name": "Analytical Thinking",    "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "Minitab / SAS (Statistical Analysis)", "mentions": 8, "rank": 1},
                {"name": "Excel / Google Sheets", "mentions": 9, "rank": 2},
                {"name": "Tableau / Power BI", "mentions": 6, "rank": 3},
            ]},
            {"name": "Documentation",          "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "ERP Quality Module (SAP QM)", "mentions": 8, "rank": 1},
                {"name": "Non-Conformance Reporting Systems", "mentions": 7, "rank": 2},
                {"name": "Digital Work Instructions", "mentions": 7, "rank": 3},
            ]},
            {"name": "Communication",          "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Slack / Teams", "mentions": 7, "rank": 1},
                {"name": "SharePoint / Confluence", "mentions": 7, "rank": 2},
                {"name": "Audit Mgmt Software", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/production/quality-control-inspectors.htm"]
    },
    "CNC Machinist": {
        "job_title": "CNC Machinist", "posting_rank": 3,
        "median_salary_usd": "$45,000–$68,000", "employment_growth": "+7% (2024-2034)",
        "standard_skills": [
            {"name": "CNC Programming",        "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "G-Code / M-Code Programming", "mentions": 10, "rank": 1},
                {"name": "CAM Software (Mastercam / GibbsCAM)", "mentions": 9, "rank": 2},
                {"name": "CNC Controller (Fanuc / Siemens)", "mentions": 9, "rank": 3},
            ]},
            {"name": "Blueprint Reading",      "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "CAD (SolidWorks / AutoCAD)", "mentions": 9, "rank": 1},
                {"name": "GD&T Interpretation Tools", "mentions": 8, "rank": 2},
                {"name": "Digital Blueprint Software", "mentions": 7, "rank": 3},
            ]},
            {"name": "Metrology & Measurement","mentions": 9, "rank": 3, "tech_skills": [
                {"name": "CMM / Profilometer", "mentions": 8, "rank": 1},
                {"name": "Digital Calipers / Micrometers", "mentions": 9, "rank": 2},
                {"name": "SPC Software (Minitab)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Problem Solving",        "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Toolpath Simulation Software", "mentions": 8, "rank": 1},
                {"name": "MES (Production Tracking)", "mentions": 7, "rank": 2},
                {"name": "Digital Maintenance Logs", "mentions": 6, "rank": 3},
            ]},
            {"name": "Attention to Detail",    "mentions": 8, "rank": 5, "tech_skills": [
                {"name": "In-Process Gauging Systems", "mentions": 8, "rank": 1},
                {"name": "QMS / Non-Conformance Reporting", "mentions": 7, "rank": 2},
                {"name": "Tool Inventory Management Software", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/production/machinists-and-tool-and-die-makers.htm"]
    },
    "Industrial Maintenance Technician": {
        "job_title": "Industrial Maintenance Technician", "posting_rank": 4,
        "median_salary_usd": "$50,000–$75,000", "employment_growth": "+11% (2024-2034)",
        "standard_skills": [
            {"name": "Mechanical Troubleshooting","mentions": 10, "rank": 1, "tech_skills": [
                {"name": "CMMS (IBM Maximo / SAP PM)", "mentions": 9, "rank": 1},
                {"name": "Vibration Analysis Tools", "mentions": 8, "rank": 2},
                {"name": "Thermal Imaging Cameras", "mentions": 7, "rank": 3},
            ]},
            {"name": "Electrical Systems",    "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "PLC Programming (Allen-Bradley/Siemens)", "mentions": 9, "rank": 1},
                {"name": "Multimeters / Oscilloscopes", "mentions": 9, "rank": 2},
                {"name": "SCADA Systems", "mentions": 7, "rank": 3},
            ]},
            {"name": "Preventive Maintenance","mentions": 9, "rank": 3, "tech_skills": [
                {"name": "Predictive Maintenance (PdM) Software", "mentions": 8, "rank": 1},
                {"name": "IoT Sensor Platforms", "mentions": 7, "rank": 2},
                {"name": "CMMS Scheduling Tools", "mentions": 9, "rank": 3},
            ]},
            {"name": "Safety Compliance",     "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "OSHA Lockout/Tagout (LOTO) Systems", "mentions": 9, "rank": 1},
                {"name": "EHS Software (Intelex)", "mentions": 7, "rank": 2},
                {"name": "Safety Audit Apps", "mentions": 6, "rank": 3},
            ]},
            {"name": "Documentation",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "CMMS Work Order Systems", "mentions": 9, "rank": 1},
                {"name": "Digital Maintenance Logs (Tablet-based)", "mentions": 7, "rank": 2},
                {"name": "CAD / Schematic Tools", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/installation-maintenance-and-repair/"]
    },
    "Production Supervisor": {
        "job_title": "Production Supervisor", "posting_rank": 5,
        "median_salary_usd": "$60,000–$85,000", "employment_growth": "+6% (2024-2034)",
        "standard_skills": [
            {"name": "Team Leadership",       "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "Workday / SAP HCM (HR Systems)", "mentions": 8, "rank": 1},
                {"name": "Scheduling Software (Kronos)", "mentions": 8, "rank": 2},
                {"name": "KPI Dashboards (Power BI)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Production Planning",   "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "MES / ERP Production Module", "mentions": 9, "rank": 1},
                {"name": "SAP PP (Production Planning)", "mentions": 8, "rank": 2},
                {"name": "Excel / Google Sheets", "mentions": 9, "rank": 3},
            ]},
            {"name": "Quality Mindset",       "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "QMS Software (ETQ)", "mentions": 8, "rank": 1},
                {"name": "SPC / Minitab", "mentions": 7, "rank": 2},
                {"name": "Digital Audit Tools", "mentions": 6, "rank": 3},
            ]},
            {"name": "Safety Culture",        "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "EHS Software (Intelex/Cority)", "mentions": 8, "rank": 1},
                {"name": "Incident Reporting Apps", "mentions": 7, "rank": 2},
                {"name": "LOTO / Safety Compliance Tools", "mentions": 8, "rank": 3},
            ]},
            {"name": "Communication",         "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Slack / Teams", "mentions": 8, "rank": 1},
                {"name": "Shift Handover Software", "mentions": 7, "rank": 2},
                {"name": "Digital Whiteboards (Miro)", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.glassdoor.com/Career/production-supervisor-career_KO0,21.htm"]
    },

    # ── ENERGY ────────────────────────────────────────────────────────────────
    "Renewable Energy Project Manager": {
        "job_title": "Renewable Energy Project Manager", "posting_rank": 1,
        "median_salary_usd": "$95,000–$130,000", "employment_growth": "+11% (2024-2034)",
        "standard_skills": [
            {"name": "Project Management",    "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "MS Project / Primavera P6", "mentions": 9, "rank": 1},
                {"name": "Procore / PlanGrid (Construction)", "mentions": 8, "rank": 2},
                {"name": "Jira / Asana", "mentions": 7, "rank": 3},
            ]},
            {"name": "Technical Engineering Knowledge","mentions": 9, "rank": 2, "tech_skills": [
                {"name": "PVSyst (Solar Modelling)", "mentions": 9, "rank": 1},
                {"name": "WindPRO / WAsP (Wind Modelling)", "mentions": 8, "rank": 2},
                {"name": "AutoCAD / Civil 3D", "mentions": 7, "rank": 3},
                {"name": "HOMER Grid (Hybrid Systems)", "mentions": 6, "rank": 4},
            ]},
            {"name": "Stakeholder Communication","mentions": 9, "rank": 3, "tech_skills": [
                {"name": "PowerPoint / Google Slides", "mentions": 9, "rank": 1},
                {"name": "GIS Tools (ArcGIS / QGIS)", "mentions": 7, "rank": 2},
                {"name": "Permitting Software (PermitFlow)", "mentions": 6, "rank": 3},
            ]},
            {"name": "Financial Analysis",    "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Excel / Financial Modelling", "mentions": 9, "rank": 1},
                {"name": "SAP / Oracle Financials", "mentions": 7, "rank": 2},
                {"name": "LCOE Modelling Tools", "mentions": 7, "rank": 3},
            ]},
            {"name": "Regulatory Compliance", "mentions": 8, "rank": 5, "tech_skills": [
                {"name": "NERC / FERC Compliance Tools", "mentions": 8, "rank": 1},
                {"name": "Environmental Impact Assessment Software", "mentions": 7, "rank": 2},
                {"name": "GRC Platforms", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/management/construction-managers.htm"]
    },
    "Solar Panel Installer": {
        "job_title": "Solar Panel Installer", "posting_rank": 2,
        "median_salary_usd": "$44,000–$62,000", "employment_growth": "+48% (2024-2034)",
        "standard_skills": [
            {"name": "Physical Stamina & Safety","mentions": 10, "rank": 1, "tech_skills": [
                {"name": "PV System Design Software (Aurora Solar)", "mentions": 9, "rank": 1},
                {"name": "Safety Management Apps (iAuditor)", "mentions": 8, "rank": 2},
                {"name": "OSHA 10/30 Compliance Tools", "mentions": 8, "rank": 3},
            ]},
            {"name": "Electrical Knowledge",  "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Multimeters / Clamp Meters", "mentions": 9, "rank": 1},
                {"name": "NEC Code Reference Software", "mentions": 8, "rank": 2},
                {"name": "String Inverter Programming", "mentions": 7, "rank": 3},
            ]},
            {"name": "Blueprint Reading",     "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "AutoCAD (basic)", "mentions": 7, "rank": 1},
                {"name": "Aurora Solar / Helioscope", "mentions": 9, "rank": 2},
                {"name": "Tablet-Based Field Apps", "mentions": 7, "rank": 3},
            ]},
            {"name": "Attention to Detail",   "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "Drone Inspection Software", "mentions": 7, "rank": 1},
                {"name": "IV Curve Tracer Tools", "mentions": 7, "rank": 2},
                {"name": "Thermal Imaging Cameras", "mentions": 7, "rank": 3},
            ]},
            {"name": "Problem Solving",       "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "SCADA / Monitoring Platforms (SolarEdge)", "mentions": 8, "rank": 1},
                {"name": "Field Service Mgmt Apps", "mentions": 7, "rank": 2},
                {"name": "Digital Commissioning Tools", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/construction-and-extraction/solar-photovoltaic-installers.htm"]
    },
    "Wind Turbine Technician": {
        "job_title": "Wind Turbine Technician", "posting_rank": 3,
        "median_salary_usd": "$55,000–$75,000", "employment_growth": "+60% (2024-2034)",
        "standard_skills": [
            {"name": "Mechanical Aptitude",   "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "SCADA Wind Farm Monitoring", "mentions": 10, "rank": 1},
                {"name": "Vibration Analysis Tools", "mentions": 8, "rank": 2},
                {"name": "Gearbox Diagnostic Equipment", "mentions": 7, "rank": 3},
            ]},
            {"name": "Electrical Systems",    "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "PLC Systems (Siemens/ABB)", "mentions": 8, "rank": 1},
                {"name": "Power Quality Analyzers", "mentions": 7, "rank": 2},
                {"name": "Multimeters / Thermal Cameras", "mentions": 8, "rank": 3},
            ]},
            {"name": "Safety & Heights Work", "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "GWO Safety Training Platforms", "mentions": 9, "rank": 1},
                {"name": "Safety Inspection Apps (iAuditor)", "mentions": 8, "rank": 2},
                {"name": "Rescue / Fall-Arrest Systems", "mentions": 7, "rank": 3},
            ]},
            {"name": "Preventive Maintenance","mentions": 8, "rank": 4, "tech_skills": [
                {"name": "CMMS (SAP PM / Maximo)", "mentions": 9, "rank": 1},
                {"name": "Predictive Maintenance IoT", "mentions": 7, "rank": 2},
                {"name": "Digital Work Orders (Tablet)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Problem Solving",       "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "Wind Farm SCADA Analytics", "mentions": 8, "rank": 1},
                {"name": "Drone Inspection Software", "mentions": 7, "rank": 2},
                {"name": "OEM Service Manuals (Digital)", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/installation-maintenance-and-repair/wind-turbine-technicians.htm"]
    },
    "Energy Analyst": {
        "job_title": "Energy Analyst", "posting_rank": 4,
        "median_salary_usd": "$70,000–$100,000", "employment_growth": "+14% (2024-2034)",
        "standard_skills": [
            {"name": "Quantitative Analysis",  "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "Python / R (Energy Modelling)", "mentions": 9, "rank": 1},
                {"name": "HOMER / EnergyPLAN", "mentions": 8, "rank": 2},
                {"name": "SQL / Databases", "mentions": 8, "rank": 3},
                {"name": "Excel / Google Sheets", "mentions": 10, "rank": 4},
            ]},
            {"name": "Energy Markets Knowledge","mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Bloomberg / Wood Mackenzie", "mentions": 8, "rank": 1},
                {"name": "EIA Data Tools", "mentions": 8, "rank": 2},
                {"name": "PLEXOS / Aurora (Power Markets)", "mentions": 7, "rank": 3},
            ]},
            {"name": "Data Visualization",    "mentions": 8, "rank": 3, "tech_skills": [
                {"name": "Tableau / Power BI", "mentions": 9, "rank": 1},
                {"name": "Python (Plotly / Matplotlib)", "mentions": 8, "rank": 2},
                {"name": "GIS (ArcGIS / QGIS)", "mentions": 6, "rank": 3},
            ]},
            {"name": "Written Communication", "mentions": 8, "rank": 4, "tech_skills": [
                {"name": "PowerPoint / Google Slides", "mentions": 9, "rank": 1},
                {"name": "Confluence / Notion", "mentions": 7, "rank": 2},
                {"name": "LaTeX / Word (Report Writing)", "mentions": 6, "rank": 3},
            ]},
            {"name": "Critical Thinking",     "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "MATLAB / Simulink", "mentions": 7, "rank": 1},
                {"name": "Monte Carlo Simulation Tools", "mentions": 6, "rank": 2},
                {"name": "Sensitivity Analysis Software", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/life-physical-and-social-science/environmental-scientists-and-specialists.htm"]
    },
    "Petroleum Engineer": {
        "job_title": "Petroleum Engineer", "posting_rank": 5,
        "median_salary_usd": "$120,000–$160,000", "employment_growth": "+2% (2024-2034)",
        "standard_skills": [
            {"name": "Reservoir Engineering", "mentions": 10, "rank": 1, "tech_skills": [
                {"name": "Petrel / Eclipse (Reservoir Simulation)", "mentions": 10, "rank": 1},
                {"name": "CMG / tNavigator", "mentions": 8, "rank": 2},
                {"name": "Well Testing Software", "mentions": 7, "rank": 3},
            ]},
            {"name": "Drilling Engineering",  "mentions": 9, "rank": 2, "tech_skills": [
                {"name": "Landmark WellPlan / Halliburton Wellbore", "mentions": 9, "rank": 1},
                {"name": "Drilling Data Platforms (Pason)", "mentions": 8, "rank": 2},
                {"name": "MWD / LWD Tools", "mentions": 7, "rank": 3},
            ]},
            {"name": "Quantitative Analysis", "mentions": 9, "rank": 3, "tech_skills": [
                {"name": "Python / MATLAB", "mentions": 8, "rank": 1},
                {"name": "Excel / VBA (Financial Models)", "mentions": 9, "rank": 2},
                {"name": "Aries / PHDWin (Economics)", "mentions": 7, "rank": 3},
                {"name": "SQL / Database Tools", "mentions": 6, "rank": 4},
            ]},
            {"name": "Technical Communication","mentions": 7, "rank": 4, "tech_skills": [
                {"name": "PowerPoint / Google Slides", "mentions": 8, "rank": 1},
                {"name": "Petrel Reporting Module", "mentions": 7, "rank": 2},
                {"name": "Well Report Writing Tools", "mentions": 6, "rank": 3},
            ]},
            {"name": "Project Management",    "mentions": 7, "rank": 5, "tech_skills": [
                {"name": "SAP / Oracle EAM", "mentions": 8, "rank": 1},
                {"name": "MS Project / Primavera", "mentions": 7, "rank": 2},
                {"name": "Risk Management Software", "mentions": 6, "rank": 3},
            ]},
        ],
        "sources": ["https://www.bls.gov/ooh/architecture-and-engineering/petroleum-engineers.htm"]
    },
}
