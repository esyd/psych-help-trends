# psych-help-trends

> **Research project:** Analyzing Google Search trends for psychological and psychotherapeutic help-seeking behavior in Ukraine and other countries.

---

## Overview

This project investigates how internet users in Ukraine and other countries search for psychological and psychotherapeutic help, with a focus on evidence-based treatment methods (CBT, EMDR, DBT, ACT, and others).

Data is collected via the **Google Trends** public API using the `pytrends` Python library (version 4.9.2).

---

## Pre-registration and Amendments

This study is pre-registered on OSF before any data collection.  
🔗 [OSF Pre-registration](https://doi.org/10.17605/OSF.IO/7986U)

**What is pre-registered:**
- `keywords.json` — full list of search terms by category and language
- `config.py` — study parameters (countries, time range, languages)
- Hypotheses and analysis plan

⚠️ **`collect_trends.py` was NOT run before OSF registration.**  
File hashes in `data/raw_<timestamp>/metadata.json` confirm that `keywords.json` and `config.py` were not modified after registration.

**OSF Amendment (filed 2026-04-28 — before data analysis):**  
Six amendments were filed prior to data analysis:
1. H3 method revised: multiple regression → Kruskal-Wallis + Spearman + exploratory simple linear regression (N=21 insufficient for multiple regression)
2. Country group role clarified: descriptive only, not used as analytical factor
3. WHO Atlas indicator operationalised: government mental health expenditure as % of total health expenditure
4. Pew religiosity operationalised: 100 − % religiously unaffiliated (Pew 2020)
5. Sensitivity analyses added for all hypotheses re: Google Trends January 2022 methodology change (Myburgh, 2022)
6. H2b EBT ratio robustness to Google Trends 2022 change clarified

---

## Hypotheses

**H1 — Temporal dynamics (Ukraine)**  
The time series of search activity for psychological help in Ukraine shows a statistically significant break (level and/or slope) in February 2022.  
*Method: Interrupted Time Series (ITS), segmented regression*

**H2a — Absolute growth of evidence-based methods**  
Search activity for evidence-based treatments (CBT, EMDR, DBT, ACT, CPT, prolonged exposure, IPT, MBCT, MBSR, schema therapy) increases over time across studied countries.  
*Method: OLS linear trend; Mann-Kendall as alternative*

**H2b — Relative growth of evidence-based methods**  
The share of evidence-based treatment searches relative to general psychological help searches increases over time — reflecting a qualitative shift in user awareness.  
*Method: OLS linear trend on EBT ratio*

**H3 — Cross-national differences**  
Country-level search activity for psychological help and evidence-based treatments is positively associated with mental health system development, GDP per capita, and scientific output in psychology; and negatively associated with religiosity.  
*Method: Kruskal-Wallis + Spearman correlations (primary); simple linear regression (exploratory)*

---

## Countries

| Group | Countries |
|-------|-----------|
| **Focal** | 🇺🇦 UA |
| **Group A** | 🇩🇪 DE, 🇫🇷 FR, 🇵🇱 PL, 🇳🇱 NL, 🇱🇻 LV, 🇱🇹 LT, 🇪🇪 EE, 🇺🇸 US, 🇬🇧 GB, 🇦🇺 AU, 🇨🇦 CA |
| **Group B** | 🇬🇪 GE, 🇦🇲 AM, 🇦🇿 AZ, 🇰🇿 KZ, 🇺🇿 UZ, 🇲🇩 MD, 🇮🇱 IL, 🇯🇵 JP, 🇧🇷 BR |

**Excluded:** Russia (RU), Belarus (BY) — search censorship distorts data.

Total: **21 countries**

> Note: Groups A and B serve a descriptive and organisational function only; they are not used as factors in any statistical model.

---

## Predictors for H3

| Predictor | Operationalisation | Source | Year |
|-----------|-------------------|--------|------|
| Mental health system development | Government mental health expenditure as % of total government health expenditure | WHO Mental Health Atlas 2020 | 2019 |
| GDP per capita | Nominal GDP per capita (current USD), log-transformed | World Bank | 2023 |
| Scientific output in psychology | Psychology publications per 1M population | SCImago Journal & Country Rank | 2023 |
| Religiosity | 100 − % religiously unaffiliated | Pew Research Center (Hackett et al., 2025) | 2020 |

Predictor data are stored in `data/predictors/H3_predictors.csv`.

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
| Latin abbreviations (CBT, EMDR, DBT, ACT, etc.) | All |

**Limitation:** Local languages for Group B countries (except Russian), and for IL, JP, BR are not included due to inability to verify translations. This is documented as an explicit study limitation.

---

## Time range

`2018-01-01` — `2025-12-31`

Google Trends returns **monthly** data for ranges over 5 years.  
Values are relative (0–100 scale) — search interest relative to the peak within the given time range and region.

> **Important:** Google Trends updated its data collection methodology effective 1 January 2022, resulting in systematically higher RSV values from that date onward (Myburgh, 2022). Sensitivity analyses addressing this discontinuity are implemented in all analysis notebooks.

---

## Project structure

```
psych-help-trends/
├── keywords.json              # Pre-registered search terms
├── config.py                  # Pre-registered study parameters
├── collect_trends.py          # Data collection script (run AFTER registration)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── data/
│   ├── raw_<timestamp>/       # Raw collected data (not committed to git)
│   │   ├── metadata.json      # UTC timestamp + SHA-256 hashes of keywords.json and config.py
│   │   ├── UA/                # Data per country
│   │   └── ...
│   └── predictors/            # H3 predictor data (committed to git)
│       └── H3_predictors.csv  # WHO Atlas, World Bank, SCImago, Pew Research
│
└── analysis/                  # Analysis notebooks (with inline comments)
    ├── 01_data_overview.ipynb             # Data quality and overview
    ├── 02_H2a_absolute_trend.ipynb        # H2a: absolute trend in EBT searches
    ├── 03_H2b_EBT_ratio.ipynb            # H2b: relative growth of EBT searches
    ├── 04_H1_ITS_Ukraine.ipynb           # H1: ITS analysis for Ukraine
    └── 05_H3_cross_national.ipynb        # H3: cross-national analysis
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

# 6. Run analysis notebooks in order
# analysis/01_data_overview.ipynb
# analysis/02_H2a_absolute_trend.ipynb
# analysis/03_H2b_EBT_ratio.ipynb
# analysis/04_H1_ITS_Ukraine.ipynb
# analysis/05_H3_cross_national.ipynb
```

---

## Key references

Myburgh, N. (2022). Infodemiologists beware: Recent changes to the Google Health Trends API result in incomparable data as of 1 January 2022. *International Journal of Environmental Research and Public Health*, 19(22), 15396. https://doi.org/10.3390/ijerph192215396

Hackett, C., Stonawski, M., Tong, Y., Kramer, S., & Shi, A. F. (2025). Dataset of Global Religious Composition Estimates for 2010 and 2020. Pew Research Center. https://doi.org/10.58094/vhrw-k516

---

## Citation

*To be added after publication.*

---

## License

Code: [MIT](LICENSE)  
Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
