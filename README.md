# psych-help-trends

> **Research project:** Analyzing Google Search trends for psychological and psychotherapeutic help-seeking behavior in Ukraine and other countries.

---

## Overview

This project investigates how internet users in Ukraine and other countries search for psychological and psychotherapeutic help, with a focus on evidence-based treatment methods (CBT, EMDR, DBT, ACT).

Data is collected via the **Google Trends** public API using the `pytrends` Python library.

---

## Hypotheses

**H1 — Temporal dynamics (Ukraine)**
The time series of search activity for psychological help in Ukraine shows a statistically significant break (level and/or slope) in February 2022.
*Method: Interrupted Time Series (ITS)*

**H2a — Absolute growth of evidence-based methods**
Search activity for evidence-based treatments (CBT, EMDR, DBT, ACT) increases over time across studied countries.

**H2b — Relative growth of evidence-based methods**
The share of evidence-based treatment searches relative to general psychological help searches increases over time — reflecting a qualitative shift in user awareness.

**H3 — Cross-national differences**
The level of search activity for psychological help and evidence-based treatments is:
- positively associated with mental health system development (WHO Atlas), GDP per capita, and scientific output in psychology
- negatively associated with religiosity (Pew Research)

---

## Pre-registration

This study is pre-registered on OSF before any data collection.  
🔗 [OSF Pre-registration](https://doi.org/10.17605/OSF.IO/7986U)

**What is pre-registered:**
- `keywords.json` — full list of search terms by category and language
- `config.py` — study parameters (countries, time range, languages)
- Hypotheses and analysis plan (this README)

⚠️ **`collect_trends.py` was NOT run before OSF registration.**  
File hashes in `data/raw_<timestamp>/metadata.json` confirm that `keywords.json` and `config.py` were not modified after registration.

---

## Countries

| Group | Countries |
|-------|-----------|
| **Focal** | 🇺🇦 UA |
| **Group A** | 🇩🇪 DE, 🇫🇷 FR, 🇵🇱 PL, 🇳🇱 NL, 🇱🇻 LV, 🇱🇹 LT, 🇪🇪 EE, 🇺🇸 US, 🇬🇧 GB, 🇦🇺 AU, 🇨🇦 CA |
| **Group B** | 🇬🇪 GE, 🇦🇲 AM, 🇦🇿 AZ, 🇰🇿 KZ, 🇺🇿 UZ, 🇲🇩 MD, 🇮🇱 IL, 🇯🇵 JP, 🇧🇷 BR |

**Excluded:** Russia (RU), Belarus (BY) — search censorship distorts data.

Total: **21 countries**

---

## Predictors for H3

| Predictor | Type | Source |
|-----------|------|--------|
| Mental health system development | Continuous | WHO Mental Health Atlas 2020 |
| GDP per capita | Continuous | World Bank |
| Scientific output in psychology | Continuous | SCImago / Scopus |
| Religiosity index | Continuous | Pew Research Global |

---

## Languages

| Language | Countries |
|----------|-----------|
| Ukrainian (uk) | UA |
| Russian (ru) | UA, LV, LT, EE, GE, AM, AZ, KZ, UZ, MD |
| English (en) | All |
| German (de) | DE |
| French (fr) | FR |
| Polish (pl) | PL |
| Dutch (nl) | NL |
| Latvian (lv) | LV |
| Lithuanian (lt) | LT |
| Estonian (et) | EE |
| Latin abbreviations (CBT, EMDR, DBT, ACT) | All |

**Limitation:** Local languages for Group B (except Russian) and IL, JP, BR are not included due to inability to verify translations. This is documented as an explicit study limitation.

---

## Time range

`2018-01-01` — `2025-12-31`

Google Trends returns **monthly** data for ranges over 5 years.  
Values are relative (0–100 scale) — search interest relative to the peak within the given time range and region.

---

## Project structure

```
psych-help-trends/
├── keywords.json       # Pre-registered search terms
├── config.py           # Pre-registered study parameters
├── collect_trends.py   # Data collection script (run AFTER registration)
├── requirements.txt    # Python dependencies
├── data/               # Raw collected data (not committed to git)
│   └── raw_<timestamp>/
│       ├── metadata.json   # Timestamp + SHA-256 hashes of keywords.json and config.py
│       ├── UA/             # Data per country
│       └── ...
└── analysis/           # Analysis scripts (to be added after data collection)
```

---

## Reproducibility

Every data collection run saves `metadata.json` containing:
- UTC timestamp of collection
- All config parameters
- SHA-256 hashes of `keywords.json` and `config.py`

This allows verification that collected data matches the pre-registered protocol.

---

## How to reproduce

```bash
# 1. Clone the repository
git clone https://github.com/esyd/psych-help-trends.git
cd psych-help-trends

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Review pre-registered parameters
# keywords.json — search terms
# config.py     — countries, time range, languages

# 5. Run data collection
python collect_trends.py

# Output: data/raw_<timestamp>/
```

---

## Citation

*To be added after publication.*

---

## License

Code: [MIT](LICENSE)  
Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
