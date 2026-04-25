# 🗺️ Operational Risk Heatmap & Control Effectiveness Scoring

> Quantitative control effectiveness scoring model and interactive risk heatmap — assessing the integrity of internal controls across business units, aligned to Chief Controls Office (CCO) framework logic.

---

## 📌 Business Problem

Banks operate thousands of internal controls across business units. Without a systematic scoring framework, identifying which controls are weakest and where risk is concentrated is subjective and inconsistent. This project builds a quantitative scoring engine and visual heatmap to surface control weaknesses objectively — enabling risk-prioritised decision-making and escalation to senior management.

---

## 🎯 Objectives

- Score each control quantitatively across multiple risk dimensions
- Identify and rank the weakest controls for escalation
- Visualise risk concentration via an interactive heatmap by business unit and risk type
- Produce RAG-status MI reports aligned to CCO reporting standards
- Extract and transform risk data using SQL pipelines

---

## 🏗️ Project Architecture

```
Control Assessment Data → SQL Extraction → Preprocessing
                       → Scoring Engine (Multi-dimensional)
                       → Risk Heatmap + RAG Dashboard
                       → MI Report Output
```

---

## 🔬 Methodology

### 1. Data
- Synthetic control assessment dataset across 6 business units and 7 risk dimensions
- Fields: control_id, business_unit, control_type, risk_dimension, assessment_score, frequency_of_failure, regulatory_impact, operational_impact

### 2. Scoring Engine
Composite effectiveness score (0–100) across 5 weighted dimensions:

| Dimension | Weight |
|---|---|
| Assessment score | 35% |
| Frequency of failure | 25% |
| Regulatory impact | 20% |
| Operational impact | 15% |
| Assessment staleness | 5% |

### 3. Risk Rating
- **Low Risk** — score ≥ 80
- **Medium Risk** — score 60–79
- **High Risk** — score 40–59
- **Critical Risk** — score < 40

### 4. RAG Status
Green / Amber / Red status for Power BI dashboard reporting to control owners and senior management.

### 5. SQL Pipelines
- Business unit effectiveness summaries
- Top 10 weakest controls for escalation
- Risk heatmap cross-tab (business unit vs risk dimension)
- Automated vs manual control comparison
- Controls overdue for reassessment

---

## 📊 Results

| Metric | Value |
|---|---|
| Controls assessed | 15 |
| Average effectiveness score | 68.4 / 100 |
| Red (critical/high risk) controls | 4 |
| Amber (medium risk) controls | 6 |
| Green (low risk) controls | 5 |

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.10 · SQL |
| Scoring | Pandas · NumPy |
| Visualisation | Power BI (DAX) · Matplotlib · Seaborn |
| Data Extraction | SQL (CTEs, Window Functions, DATEDIFF) |
| Reporting | Structured MI Reports |

---

## 📂 Repository Structure

```
├── data/
│   └── control_assessments.csv       # Synthetic control assessment data
├── notebooks/
│   ├── 01_eda_control_data.ipynb
│   └── 02_scoring_and_heatmap.ipynb
├── src/
│   ├── preprocess.py                 # Data loading & preprocessing
│   ├── scoring_engine.py             # Multi-dimensional scoring model
│   └── sql_queries.sql               # SQL extraction & transformation pipelines
├── reports/                          # MI reports & dashboard screenshots
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

```bash
git clone https://github.com/zaidmohd070331/operational-risk-heatmap.git
cd operational-risk-heatmap
pip install -r requirements.txt
python src/preprocess.py
python src/scoring_engine.py
```

---

## 💡 Key Takeaways

- Multi-dimensional scoring is more robust than single-metric assessments
- RAG status enables instant visual triage for non-technical stakeholders
- SQL pipelines ensure reproducibility and auditability of data extraction
- Scoring methodology directly mirrors CCO control assessment frameworks

---
