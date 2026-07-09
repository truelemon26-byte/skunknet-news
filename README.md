# SkunkNet GitHub News Wire

Offloads RSS fetch, full-article extraction, and categorisation to **GitHub Actions**.
Your Rust / Carbon server only downloads one ready-made JSON file:

```
https://raw.githubusercontent.com/<USER>/<REPO>/main/skunknet_news.json
```

## Setup (one-time)

1. Create a **public** GitHub repository (example name: `skunknet-news`).
2. Push this folder’s contents to the repo root (`main` branch):
   - `.github/workflows/scrape_news.yml`
   - `scripts/scrape_news.py`
   - `requirements.txt`
   - `skunknet_news.json` (placeholder; overwritten by the bot)
3. In GitHub → **Actions** → enable workflows → run **Sync Categorized SkunkNet News** once (`workflow_dispatch`).
4. In `SkunkCore_NewsJournalist.json` set:

```json
"World news: GitHub raw JSON URL": "https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/skunknet_news.json",
"Use GitHub news JSON as world wire": true
```

5. Reload the plugin: `c.reload SkunkCore_NewsJournalist` then `sn.news.digest`.

## Schedule

- Cron: every **12 hours** (`0 */12 * * *`)
- Manual: Actions → Sync Categorized SkunkNet News → Run workflow

If Actions jobs fail instantly with **no steps** / `runner_id: 0`, GitHub has usually **locked the account for billing**. Fix billing at https://github.com/settings/billing — until then, run locally:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/scrape_news.py
git add skunknet_news.json && git commit -m "Manual news sync" && git push
```

## JSON shape (plugin reads these first)

| Key | SkunkOS News tab (UI label) |
|-----|-----------------------------|
| `Breaking` | Breaking |
| `Business` | Finance |
| `Sports` | Sports |
| `Gaming_Tech` | Technology |
| `Entertainment` | Entertainment |

Each article:

```json
{
  "title": "...",
  "text": "full article body",
  "description": "short blurb",
  "source_url": "https://...",
  "category": "Business",
  "author": "SkunkNet Wire - bbc.co.uk",
  "breaking": false,
  "publishedUnix": 1720000000,
  "source": "bbc.co.uk"
}
```

Guide-style aliases (`BreakingNewsTab`, `FinanceTab`, …) are also written for tooling.

## Safety

- No third-party news APIs on the game server
- No Python / HTML scraping on the game server
- Single async `webrequest.Enqueue` to `raw.githubusercontent.com`
