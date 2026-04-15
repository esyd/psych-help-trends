"""
collect_trends.py
-----------------
Data collection script for the psych-help-trends project.

⚠️  DO NOT RUN before pre-registration on OSF.
    Pre-register keywords.json + config.py first.

Usage:
    python collect_trends.py

Output:
    data/raw_<timestamp>/   — one CSV per keyword category + metadata.json
"""

import json
import time
import logging
import hashlib
from pathlib import Path
from datetime import datetime

import pandas as pd
from pytrends.request import TrendReq

import config

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("collection.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)


# ── Helpers ────────────────────────────────────────────────────────────────────

def load_keywords(path: str = "keywords.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["categories"]


def file_hash(path: str) -> str:
    """SHA-256 hash of a file — for reproducibility checks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def flatten_terms(categories: dict, languages: list) -> list[dict]:
    """
    Returns a flat list of {category, language, term} dicts
    for all combinations in the config.
    """
    result = []
    for cat_name, cat_data in categories.items():
        for lang in languages:
            terms = cat_data.get("terms", {}).get(lang, [])
            for term in terms:
                result.append({
                    "category": cat_name,
                    "language": lang,
                    "term": term,
                })
    return result


# ── Core collection ────────────────────────────────────────────────────────────

def collect_trend(
    pytrends: TrendReq,
    terms: list[str],
    geo: str,
    timeframe: str,
    cat: int = 0,
    gprop: str = "",
) -> pd.DataFrame | None:
    """
    Fetch interest-over-time for up to 5 terms at once (Google Trends limit).
    Returns a DataFrame or None if the request fails.
    """
    try:
        pytrends.build_payload(
            kw_list=terms,
            cat=cat,
            timeframe=timeframe,
            geo=geo,
            gprop=gprop,
        )
        df = pytrends.interest_over_time()
        if df.empty:
            log.warning(f"No data returned for terms: {terms} | geo: {geo}")
            return None
        df = df.drop(columns=["isPartial"], errors="ignore")
        return df
    except Exception as e:
        log.error(f"Error fetching {terms} for geo={geo}: {e}")
        return None


def collect_related_queries(
    pytrends: TrendReq,
    terms: list[str],
    geo: str,
    timeframe: str,
) -> dict:
    """
    Fetch related queries (top + rising) for given terms.
    """
    try:
        pytrends.build_payload(
            kw_list=terms,
            timeframe=timeframe,
            geo=geo,
        )
        return pytrends.related_queries()
    except Exception as e:
        log.error(f"Error fetching related queries for {terms}: {e}")
        return {}


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(config.OUTPUT_DIR) / f"raw_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Output directory: {out_dir}")

    # ── Save metadata ──────────────────────────────────────────────────────────
    metadata = {
        "collection_timestamp_utc": timestamp,
        "config": {
            "geo_primary": config.GEO_PRIMARY,
            "geo_comparison": config.GEO_COMPARISON,
            "timeframe": config.TIMEFRAME,
            "languages": config.LANGUAGES,
            "trends_category": config.TRENDS_CATEGORY,
            "trends_gprop": config.TRENDS_GPROP,
        },
        "file_hashes": {
            "keywords.json": file_hash("keywords.json"),
            "config.py": file_hash("config.py"),
        },
    }
    with open(out_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    log.info(f"Metadata saved: {out_dir / 'metadata.json'}")

    # ── Load keywords ──────────────────────────────────────────────────────────
    categories = load_keywords("keywords.json")
    flat_terms = flatten_terms(categories, config.LANGUAGES)
    log.info(f"Total terms to collect: {len(flat_terms)}")

    # ── Init pytrends ──────────────────────────────────────────────────────────
    pytrends = TrendReq(hl="uk", tz=120, timeout=(10, 25), retries=3, backoff_factor=0.5)

    # ── Collect for primary geo ────────────────────────────────────────────────
    all_geos = [config.GEO_PRIMARY] + config.GEO_COMPARISON

    for geo in all_geos:
        log.info(f"=== Collecting for GEO: {geo} ===")
        geo_dir = out_dir / geo
        geo_dir.mkdir(exist_ok=True)

        # Group by category + language (max 5 terms per request)
        from itertools import groupby
        grouped = {}
        for item in flat_terms:
            key = (item["category"], item["language"])
            grouped.setdefault(key, []).append(item["term"])

        for (cat_name, lang), terms in grouped.items():
            # Google Trends allows max 5 keywords per request
            chunks = [terms[i:i+5] for i in range(0, len(terms), 5)]

            for chunk_idx, chunk in enumerate(chunks):
                log.info(f"  [{geo}] {cat_name}/{lang} chunk {chunk_idx+1}: {chunk}")

                df = collect_trend(
                    pytrends,
                    chunk,
                    geo=geo,
                    timeframe=config.TIMEFRAME,
                    cat=config.TRENDS_CATEGORY,
                    gprop=config.TRENDS_GPROP,
                )

                if df is not None:
                    fname = f"{cat_name}__{lang}__chunk{chunk_idx+1}.csv"
                    df.to_csv(geo_dir / fname)
                    log.info(f"    Saved: {fname}")

                # Related queries (only for first chunk to limit API calls)
                if chunk_idx == 0:
                    related = collect_related_queries(pytrends, chunk, geo, config.TIMEFRAME)
                    if related:
                        rq_fname = f"{cat_name}__{lang}__related.json"
                        with open(geo_dir / rq_fname, "w", encoding="utf-8") as f:
                            # Convert DataFrames to JSON-serializable format
                            serializable = {}
                            for term, data in related.items():
                                serializable[term] = {
                                    "top": data.get("top", pd.DataFrame()).to_dict() if data.get("top") is not None else {},
                                    "rising": data.get("rising", pd.DataFrame()).to_dict() if data.get("rising") is not None else {},
                                }
                            json.dump(serializable, f, indent=2, ensure_ascii=False)

                # ⚠️ Rate limiting — be polite to Google's API
                time.sleep(5)

    log.info("✅ Collection complete.")
    log.info(f"All data saved in: {out_dir}")


if __name__ == "__main__":
    main()
