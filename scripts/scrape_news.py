#!/usr/bin/env python3
"""
SkunkNet world-wire extractor (runs on GitHub Actions only).

Pulls RSS → extracts full article text with newspaper4k → categorises into
SkunkOS News tabs → writes skunknet_news.json for the Rust plugin to download.

Tab IDs match SkunkCore_UI / SkunkCore_NewsJournalist:
  Breaking, Business (Finance), Sports, Gaming_Tech (Technology), Entertainment
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import feedparser
import nltk
from newspaper import Article, Config as NewspaperConfig

# ---------------------------------------------------------------------------
# Paths / constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "skunknet_news.json"
SCHEMA_VERSION = 2

# Per-tab soft caps (plugin also clamps via MaxArticlesPerWireFeed).
MAX_PER_TAB = 14
# How many RSS entries to attempt per feed before moving on.
ENTRIES_PER_FEED = 8
# Hard ceiling on total article download attempts (Actions minute budget).
MAX_ARTICLE_FETCHES = 90
ARTICLE_TIMEOUT_SEC = 18
USER_AGENT = (
    "Mozilla/5.0 (compatible; SkunkNetNewsBot/1.0; +https://github.com/)"
)

# Canonical UI tab ids (do not rename — plugin + UI depend on these).
TAB_BREAKING = "Breaking"
TAB_FINANCE = "Business"          # UI label: Finance
TAB_SPORTS = "Sports"
TAB_TECH = "Gaming_Tech"          # UI label: Technology
TAB_ENTERTAINMENT = "Entertainment"

ALL_TABS = (TAB_BREAKING, TAB_FINANCE, TAB_SPORTS, TAB_TECH, TAB_ENTERTAINMENT)

# Guide-compatible aliases also written into the JSON for readability / tooling.
ALIAS_KEYS = {
    TAB_BREAKING: "BreakingNewsTab",
    TAB_FINANCE: "FinanceTab",
    TAB_SPORTS: "SportsTab",
    TAB_TECH: "TechnologyTab",
    TAB_ENTERTAINMENT: "EntertainmentTab",
}

# ---------------------------------------------------------------------------
# Feed matrix — category-specific RSS so every tab stays stocked
# ---------------------------------------------------------------------------

FEEDS: list[dict[str, Any]] = [
    # Breaking / world
    {"url": "http://feeds.bbci.co.uk/news/rss.xml", "hint": TAB_BREAKING},
    {"url": "http://feeds.bbci.co.uk/news/world/rss.xml", "hint": TAB_BREAKING},
    {"url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "hint": TAB_BREAKING},
    {"url": "https://feeds.reuters.com/reuters/topNews", "hint": TAB_BREAKING},
    {"url": "https://www.theguardian.com/world/rss", "hint": TAB_BREAKING},
    # Finance
    {"url": "http://feeds.bbci.co.uk/news/business/rss.xml", "hint": TAB_FINANCE},
    {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "hint": TAB_FINANCE},
    {"url": "https://feeds.reuters.com/reuters/businessNews", "hint": TAB_FINANCE},
    {"url": "https://www.theguardian.com/business/rss", "hint": TAB_FINANCE},
    {"url": "https://www.cnbc.com/id/100003114/device/rss/rss.html", "hint": TAB_FINANCE},
    # Sports
    {"url": "http://feeds.bbci.co.uk/sport/rss.xml", "hint": TAB_SPORTS},
    {"url": "https://www.espn.com/espn/rss/news", "hint": TAB_SPORTS},
    {"url": "https://www.theguardian.com/sport/rss", "hint": TAB_SPORTS},
    {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml", "hint": TAB_SPORTS},
    # Technology
    {"url": "http://feeds.bbci.co.uk/news/technology/rss.xml", "hint": TAB_TECH},
    {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "hint": TAB_TECH},
    {"url": "https://www.theguardian.com/technology/rss", "hint": TAB_TECH},
    {"url": "https://feeds.arstechnica.com/arstechnica/index", "hint": TAB_TECH},
    {"url": "https://www.theverge.com/rss/index.xml", "hint": TAB_TECH},
    # Entertainment
    {"url": "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml", "hint": TAB_ENTERTAINMENT},
    {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml", "hint": TAB_ENTERTAINMENT},
    {"url": "https://www.theguardian.com/uk/culture/rss", "hint": TAB_ENTERTAINMENT},
    {"url": "https://www.hollywood.co.uk/rss", "hint": TAB_ENTERTAINMENT},
]

# Keyword buckets (title + keywords + tags + summary)
KW_SPORTS = {
    "sport", "sports", "football", "soccer", "nba", "nfl", "mlb", "nhl",
    "premier league", "champions league", "basketball", "tennis", "golf",
    "cricket", "rugby", "mma", "ufc", "boxing", "racing", "f1", "formula 1",
    "olympics", "athletics", "wimbledon", "world cup", "match", "fixture",
}
KW_FINANCE = {
    "finance", "financial", "economy", "economic", "stocks", "stock market",
    "markets", "market", "bitcoin", "crypto", "cryptocurrency", "banking",
    "bank", "inflation", "interest rate", "federal reserve", "wall street",
    "nasdaq", "dow jones", "ftse", "gdp", "recession", "earnings", "ipo",
    "shares", "investor", "investment", "treasury", "currency", "forex",
}
KW_TECH = {
    "technology", "tech", "ai", "artificial intelligence", "software",
    "hardware", "semiconductor", "chip", "apple", "google", "microsoft",
    "meta", "amazon", "nvidia", "cyber", "hacker", "smartphone", "iphone",
    "android", "gaming", "esports", "video game", "playstation", "xbox",
    "nintendo", "startup", "silicon valley", "robot", "spaceX", "nasa",
}
KW_ENTERTAINMENT = {
    "entertainment", "hollywood", "hollywoodwood", "film", "movie", "cinema",
    "netflix", "streaming", "music", "album", "concert", "celebrity",
    "actor", "actress", "television", "tv show", "series", "oscars",
    "bafta", "grammy", "box office", "disney", "marvel", "theatre",
}
KW_BREAKING = {
    "breaking", "urgent", "disaster", "explosion", "attack", "earthquake",
    "hurricane", "wildfire", "massacre", "hostage", "emergency", "crash",
    "shooting", "war", "invasion", "missile", "terror",
}


def ensure_nltk() -> None:
    for pkg in ("punkt_tab", "punkt"):
        try:
            nltk.data.find(f"tokenizers/{pkg}")
        except LookupError:
            nltk.download(pkg, quiet=True)


def newspaper_config() -> NewspaperConfig:
    cfg = NewspaperConfig()
    cfg.browser_user_agent = USER_AGENT
    cfg.request_timeout = ARTICLE_TIMEOUT_SEC
    cfg.fetch_images = False
    cfg.memoize_articles = False
    cfg.number_threads = 1
    return cfg


def clean_text(s: str | None, limit: int = 12000) -> str:
    if not s:
        return ""
    t = re.sub(r"\s+", " ", str(s)).strip()
    if len(t) > limit:
        t = t[: limit - 1].rsplit(" ", 1)[0] + "…"
    return t


def host_of(url: str) -> str:
    try:
        h = urlparse(url).netloc.lower()
        if h.startswith("www."):
            h = h[4:]
        return h or "wire"
    except Exception:
        return "wire"


def parse_published_unix(entry: dict[str, Any], art: Article | None) -> int:
    for key in ("published", "updated", "created"):
        raw = entry.get(key)
        if not raw:
            continue
        try:
            dt = parsedate_to_datetime(raw)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except Exception:
            pass
    if art is not None and getattr(art, "publish_date", None):
        try:
            dt = art.publish_date
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except Exception:
            pass
    return int(time.time())


def blob_for_classify(title: str, summary: str, keywords: list[str], tags: list[str]) -> str:
    parts = [title or "", summary or ""]
    parts.extend(keywords or [])
    parts.extend(tags or [])
    return " ".join(parts).lower()


def score_bucket(blob: str, words: set[str]) -> int:
    score = 0
    for w in words:
        if w in blob:
            score += 2 if " " in w else 1
    return score


def classify_tab(
    title: str,
    summary: str,
    keywords: list[str],
    tags: list[str],
    feed_hint: str | None,
) -> str:
    blob = blob_for_classify(title, summary, keywords, tags)
    scores = {
        TAB_SPORTS: score_bucket(blob, KW_SPORTS),
        TAB_FINANCE: score_bucket(blob, KW_FINANCE),
        TAB_TECH: score_bucket(blob, KW_TECH),
        TAB_ENTERTAINMENT: score_bucket(blob, KW_ENTERTAINMENT),
        TAB_BREAKING: score_bucket(blob, KW_BREAKING),
    }
    best_tab, best_score = max(scores.items(), key=lambda kv: kv[1])
    if best_score >= 2:
        return best_tab
    # Trust category-specific feed when keywords are weak.
    if feed_hint in ALL_TABS:
        return feed_hint
    return TAB_BREAKING


def extract_article(url: str, cfg: NewspaperConfig) -> Article | None:
    try:
        art = Article(url, config=cfg)
        art.download()
        art.parse()
        try:
            art.nlp()
        except Exception:
            # Keywords optional — title/text still usable.
            pass
        if not art.title or not (art.text and len(art.text.strip()) > 80):
            return None
        return art
    except Exception:
        return None


def article_fingerprint(title: str, url: str) -> str:
    key = f"{(title or '').strip().lower()}|{urlparse(url).path.lower()}"
    return hashlib.sha1(key.encode("utf-8", errors="ignore")).hexdigest()


def build_payload_article(
    title: str,
    text: str,
    url: str,
    tab: str,
    published_unix: int,
    source_name: str,
) -> dict[str, Any]:
    body = clean_text(text, 12000)
    desc = body
    if len(desc) > 320:
        desc = desc[:317].rsplit(" ", 1)[0] + "..."
    return {
        "title": clean_text(title, 240),
        "text": body,
        "description": desc,
        "source_url": url,
        "category": tab,
        "author": f"SkunkNet Wire - {source_name}",
        "breaking": tab == TAB_BREAKING,
        "publishedUnix": published_unix,
        "source": source_name,
    }


def empty_tabs() -> dict[str, list]:
    return {t: [] for t in ALL_TABS}


def run() -> int:
    ensure_nltk()
    cfg = newspaper_config()
    tabs = empty_tabs()
    seen: set[str] = set()
    fetches = 0
    feed_ok = 0
    feed_fail = 0

    print(f"[SkunkNews] Starting extraction → {OUT_PATH}", flush=True)

    for feed in FEEDS:
        # Stop early if every tab is already full.
        if all(len(tabs[t]) >= MAX_PER_TAB for t in ALL_TABS):
            print("[SkunkNews] All tabs at capacity — stopping.", flush=True)
            break
        if fetches >= MAX_ARTICLE_FETCHES:
            print("[SkunkNews] Fetch budget exhausted.", flush=True)
            break

        url = feed["url"]
        hint = feed.get("hint")
        print(f"[SkunkNews] Feed: {url}", flush=True)
        try:
            parsed = feedparser.parse(url, agent=USER_AGENT)
        except Exception as ex:
            feed_fail += 1
            print(f"  ! parse failed: {ex}", flush=True)
            continue

        if getattr(parsed, "bozo", False) and not parsed.entries:
            feed_fail += 1
            print(f"  ! empty/bozo feed: {getattr(parsed, 'bozo_exception', '')}", flush=True)
            continue

        feed_ok += 1
        for entry in parsed.entries[:ENTRIES_PER_FEED]:
            if fetches >= MAX_ARTICLE_FETCHES:
                break
            link = (entry.get("link") or "").strip()
            if not link.startswith("http"):
                continue
            title_hint = clean_text(entry.get("title") or "", 240)
            fp = article_fingerprint(title_hint, link)
            if fp in seen:
                continue

            # Skip if the hinted tab is already full and we have no strong reclass need.
            if hint in tabs and len(tabs[hint]) >= MAX_PER_TAB:
                # Still allow if other tabs need fill — classify after extract.
                if all(len(tabs[t]) >= MAX_PER_TAB for t in ALL_TABS):
                    break

            fetches += 1
            art = extract_article(link, cfg)
            if art is None:
                # Fallback: RSS summary only (still better than empty tab).
                summary = clean_text(
                    entry.get("summary") or entry.get("description") or title_hint,
                    2000,
                )
                if len(summary) < 40:
                    continue
                tags = [t.get("term", "") for t in entry.get("tags", []) if isinstance(t, dict)]
                tab = classify_tab(title_hint, summary, [], tags, hint)
                if len(tabs[tab]) >= MAX_PER_TAB:
                    continue
                seen.add(fp)
                source = host_of(link)
                tabs[tab].append(
                    build_payload_article(
                        title_hint or "Untitled",
                        summary,
                        link,
                        tab,
                        parse_published_unix(entry, None),
                        source,
                    )
                )
                print(f"  + RSS-only → {tab}: {title_hint[:70]}", flush=True)
                continue

            title = clean_text(art.title, 240)
            text = clean_text(art.text, 12000)
            keywords = [str(k).lower() for k in (art.keywords or [])]
            tags = [t.get("term", "") for t in entry.get("tags", []) if isinstance(t, dict)]
            summary = clean_text(entry.get("summary") or "", 500)
            tab = classify_tab(title, summary + " " + text[:400], keywords, tags, hint)
            if len(tabs[tab]) >= MAX_PER_TAB:
                # Try to place into feed hint if different and has room.
                if hint in tabs and hint != tab and len(tabs[hint]) < MAX_PER_TAB:
                    tab = hint
                else:
                    continue

            fp2 = article_fingerprint(title, link)
            if fp2 in seen:
                continue
            seen.add(fp2)
            source = host_of(getattr(art, "source_url", None) or link)
            tabs[tab].append(
                build_payload_article(
                    title,
                    text,
                    link,
                    tab,
                    parse_published_unix(entry, art),
                    source,
                )
            )
            print(f"  + full → {tab}: {title[:70]}", flush=True)
            time.sleep(0.35)  # polite pacing

    # Guide-style alias bags + canonical tabs.
    alias_bags = {ALIAS_KEYS[t]: tabs[t] for t in ALL_TABS}
    # Extra guide key used in the pasted sample.
    alias_bags["GeneralTab"] = list(tabs[TAB_BREAKING][:3]) + list(tabs[TAB_FINANCE][:2])

    payload = {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAtUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "SkunkNet github-news/scripts/scrape_news.py",
        "stats": {
            "feedsOk": feed_ok,
            "feedsFailed": feed_fail,
            "articleFetches": fetches,
            "counts": {t: len(tabs[t]) for t in ALL_TABS},
        },
        # Canonical keys the C# plugin reads first.
        "Breaking": tabs[TAB_BREAKING],
        "Business": tabs[TAB_FINANCE],
        "Sports": tabs[TAB_SPORTS],
        "Gaming_Tech": tabs[TAB_TECH],
        "Entertainment": tabs[TAB_ENTERTAINMENT],
        # Guide-compatible aliases.
        **alias_bags,
        # Flat list for simple consumers.
        "articles": [a for t in ALL_TABS for a in tabs[t]],
    }

    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    counts = payload["stats"]["counts"]
    print(
        f"[SkunkNews] Wrote {OUT_PATH.name} | "
        + " | ".join(f"{k}={v}" for k, v in counts.items()),
        flush=True,
    )
    # Soft success even if some tabs are thin — plugin keeps previous cache on total failure.
    if sum(counts.values()) == 0:
        print("[SkunkNews] WARNING: zero articles extracted", flush=True)
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(run())
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
