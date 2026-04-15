# config.py
# Study parameters — define BEFORE data collection and pre-registration on OSF

# ── Countries by group ─────────────────────────────────────────────────────────
# Google Trends country codes (ISO 3166-1 alpha-2)

COUNTRIES = {

    # ── Focal country ──────────────────────────────────────────────────────────
    "focal": {
        "UA": {
            "name": "Ukraine",
            "languages": ["uk", "ru", "en", "latin_abbrev"],
        },
    },

    # ── Group A ────────────────────────────────────────────────────────────────
    # EU + US + GB + AU + CA
    # Local languages included where verified
    "group_a": {
        "DE": {"name": "Germany",        "languages": ["de", "en", "latin_abbrev"]},
        "FR": {"name": "France",         "languages": ["fr", "en", "latin_abbrev"]},
        "PL": {"name": "Poland",         "languages": ["pl", "en", "latin_abbrev"]},
        "NL": {"name": "Netherlands",    "languages": ["nl", "en", "latin_abbrev"]},
        "LV": {"name": "Latvia",         "languages": ["lv", "ru", "en", "latin_abbrev"]},
        "LT": {"name": "Lithuania",      "languages": ["lt", "ru", "en", "latin_abbrev"]},
        "EE": {"name": "Estonia",        "languages": ["et", "ru", "en", "latin_abbrev"]},
        "US": {"name": "United States",  "languages": ["en", "latin_abbrev"]},
        "GB": {"name": "United Kingdom", "languages": ["en", "latin_abbrev"]},
        "AU": {"name": "Australia",      "languages": ["en", "latin_abbrev"]},
        "CA": {"name": "Canada",         "languages": ["en", "latin_abbrev"]},
    },

    # ── Group B ────────────────────────────────────────────────────────────────
    # Post-Soviet non-EU + other regions
    # Local languages NOT included — translation not verified (study limitation)
    # Post-Soviet countries: Russian used as lingua franca
    "group_b": {
        "GE": {"name": "Georgia",    "languages": ["ru", "en", "latin_abbrev"]},
        "AM": {"name": "Armenia",    "languages": ["ru", "en", "latin_abbrev"]},
        "AZ": {"name": "Azerbaijan", "languages": ["ru", "en", "latin_abbrev"]},
        "KZ": {"name": "Kazakhstan", "languages": ["ru", "en", "latin_abbrev"]},
        "UZ": {"name": "Uzbekistan", "languages": ["ru", "en", "latin_abbrev"]},
        "MD": {"name": "Moldova",    "languages": ["ru", "en", "latin_abbrev"]},
        "IL": {"name": "Israel",     "languages": ["en", "latin_abbrev"]},
        "JP": {"name": "Japan",      "languages": ["en", "latin_abbrev"]},
        "BR": {"name": "Brazil",     "languages": ["en", "latin_abbrev"]},
    },
}

# Exclusions (explicit, with reason)
EXCLUDED_COUNTRIES = {
    "RU": "Search censorship distorts data",
    "BY": "Search censorship distorts data",
}

# ── Time range ─────────────────────────────────────────────────────────────────
TIMEFRAME = "2018-01-01 2025-12-31"

# ── Google Trends API settings ─────────────────────────────────────────────────
TRENDS_CATEGORY = 0     # 0 = all categories; 45 = Health
TRENDS_GPROP    = ""    # "" = web search; "youtube" = YouTube search

# ── Output ─────────────────────────────────────────────────────────────────────
OUTPUT_DIR    = "data"
OUTPUT_FORMAT = "csv"

# ── Reproducibility ────────────────────────────────────────────────────────────
RANDOM_SEED      = 42
COLLECTION_DATE  = None  # Auto-set during collection — do not change manually
