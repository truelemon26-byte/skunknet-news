#!/usr/bin/env python3
"""Seed skunknet_news.json with full multi-paragraph sample stories (no ads, no one-liners)."""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "skunknet_news.json"

PARAS = (
    "Investigators and desk editors compiled the latest verified details overnight, "
    "cross-checking official statements against on-the-ground reporting before publication.\n\n"
    "Sources familiar with the situation said developments remain fluid, with follow-up briefings "
    "expected as more information is confirmed by primary agencies and licensed wire partners.\n\n"
    "SkunkNet Wire is publishing the full available narrative for terminal readers — not a truncated "
    "headline stub — so the in-game News reader can paginate the complete report without ads, "
    "subscribe prompts, or promotional chrome."
)


def story(title: str, lead: str) -> tuple[str, str]:
    body = f"{lead.strip()}\n\n{PARAS}"
    return title, body


TABS = {
    "Breaking": [
        story("Island Alert: Global Markets Brace for Policy Shift",
              "World leaders signal coordinated action as overnight market moves ripple through major exchanges. Analysts say the next forty-eight hours will set the tone for risk assets from equities to commodities."),
        story("Emergency Services Mobilise After Coastal Storm Surge",
              "Coastal communities remain on high alert after overnight storm surges damaged harbour infrastructure and flooded low-lying roads. Authorities urged residents to avoid flooded routes while crews restore power."),
        story("Diplomatic Talks Resume After Overnight Escalation",
              "Negotiators returned to the table after overnight clashes raised fears of a wider confrontation. Envoys pressed for an immediate de-escalation and a verified ceasefire corridor for civilians."),
        story("Major Airport Disruptions Follow System Outage",
              "A cascading software failure grounded flights across several hubs for more than three hours, leaving thousands of passengers stranded as engineers restored core scheduling systems."),
        story("Rescue Teams Reach Isolated Mountain Communities",
              "Helicopter crews finally reached villages cut off by landslides after days of heavy rain. Medics treated injuries on site and evacuated critically ill patients to regional hospitals."),
        story("Government Issues Travel Advisory for Storm Corridor",
              "Transport ministries issued a formal advisory covering coastal highways and ferry routes expected to face gale-force winds. Drivers were told to postpone non-essential journeys."),
        story("Live Updates: Capital City Declares Temporary Curfew",
              "City authorities declared a temporary overnight curfew after unrest damaged several commercial blocks. Police said the measure was designed to protect emergency workers and cleanup crews."),
        story("International Aid Flights Diverted to Regional Hub",
              "Aid flights carrying medical kits and shelter materials were diverted to a regional hub after the primary runway was closed for repairs. Logistics teams reorganised last-mile distribution."),
        story("Power Grid Stabilises After Multi-State Blackout Scare",
              "Grid operators restored normal frequency after a cascading fault briefly darkened parts of three states. Automatic protections isolated the fault before it could spread further."),
        story("Security Sweep Clears Downtown After Suspicious Package",
              "Bomb disposal teams cleared a busy downtown plaza after a suspicious package prompted an evacuation of nearby offices. The device was later declared a false alarm."),
    ],
    "Business": [
        story("Central Bank Holds Rates as Inflation Cools",
              "Policymakers kept benchmark rates unchanged, citing cooler inflation prints and a desire to assess labour-market data before the next meeting."),
        story("Tech Earnings Lift Equity Futures",
              "Futures climbed after a cluster of technology firms beat revenue estimates, with chipmakers leading the advance on stronger AI spending guidance."),
        story("Oil Prices Slip on Inventory Surprise",
              "Crude benchmarks slipped after weekly inventory data showed a larger-than-expected build at key hubs, while refining margins softened into the shoulder season."),
        story("Retail Sales Beat Forecasts in Key Markets",
              "Consumer spending surprised to the upside in several large economies, led by discretionary categories that had softened earlier in the year."),
        story("Banking Sector Posts Stronger Loan Growth",
              "Major lenders reported faster loan growth alongside stable deposit bases, easing concerns about funding stress as net interest margins held up."),
        story("Currency Markets Steady Ahead of Jobs Data",
              "Foreign-exchange markets traded in tight ranges ahead of a pivotal employment report as speculators reduced leveraged positions."),
        story("Startup Funding Rebounds in Second Quarter",
              "Venture funding rebounded from a multi-quarter trough as late-stage rounds returned and corporate venture arms re-engaged with AI infrastructure deals."),
        story("Bond Yields Ease as Soft Landing Bets Rise",
              "Government bond yields eased as investors leaned into soft-landing scenarios following cooler inflation and resilient growth data."),
        story("Manufacturing PMI Edges Back Into Expansion",
              "Factory surveys edged back above the expansion threshold as new orders stabilised and supplier delivery times normalised across key exporters."),
        story("Commodity Traders Watch Shipping Lane Delays",
              "Commodity desks monitored delays along critical shipping lanes after weather and security incidents slowed transit times and lifted freight rates."),
    ],
    "Sports": [
        story("Derby Thriller Ends in Last-Minute Equaliser",
              "A packed stadium erupted as the visitors snatched a point in stoppage time, keeping both sides in the title conversation after a scrambled corner."),
        story("Grand Slam Favourite Advances in Straight Sets",
              "The top seed needed just seventy-eight minutes to book a quarter-final berth, mixing heavy groundstrokes with clinical serving throughout."),
        story("Title Contenders Trade Blows in Night Fixture",
              "Two championship contenders traded momentum swings in a night fixture that finished level after a breathless final quarter of play."),
        story("Transfer Window Buzz Intensifies Around Star Midfielder",
              "Clubs across the top flight intensified interest in a creative midfielder entering the final year of a contract as valuations remain far apart."),
        story("Olympic Hopeful Breaks National Record in Trials",
              "An Olympic hopeful shattered a long-standing national record at the selection trials, posting a time that would have medalled at the previous Games."),
        story("Coach Praises Squad Depth After Away Win",
              "A visiting coach praised squad depth after rotation players delivered a controlled away win against a direct rival in the standings."),
        story("Injury Update Clouds Weekend Line-Up Plans",
              "Medical staff provided a cautious update on two first-team regulars nursing soft-tissue injuries ahead of a pivotal weekend fixture."),
        story("Underdogs Stun League Leaders in Cup Upset",
              "Lower-league underdogs produced a famous cup upset, eliminating the league leaders with a late counterattack and composed finish."),
        story("Marathon Course Record Falls in City Race",
              "A city marathon record fell as elite fields benefited from cool temperatures and a revised, faster course through the downtown loop."),
        story("Broadcast Deal Extends Live Coverage Package",
              "A multi-year broadcast deal extended live coverage packages for domestic leagues and cup competitions with upgraded camera technology."),
    ],
    "Gaming_Tech": [
        story("Chipmaker Unveils Next-Gen AI Accelerator",
              "A leading chipmaker unveiled its next-generation AI accelerator, claiming doubled inference throughput for large language models while cutting rack power draw."),
        story("Studio Delays Flagship Title to Polish Multiplayer",
              "A major studio delayed its flagship title by six weeks to polish multiplayer stability after internal playtests exposed matchmaking edge cases."),
        story("Open-Source Model Tops Independent Benchmark Suite",
              "An open-source language model topped an independent benchmark suite covering reasoning, coding, and multilingual tasks after denser data curation."),
        story("Cloud Provider Cuts Inference Pricing for Startups",
              "A major cloud provider cut inference pricing for early-stage startups, aiming to lower barriers for product experimentation on GPU capacity."),
        story("Handheld Console Firmware Adds Performance Mode",
              "Handheld console makers shipped a firmware update adding a performance mode that raises frame-rate targets for select demanding titles."),
        story("Security Researchers Flag Critical Browser Flaw",
              "Security researchers disclosed a critical browser flaw that could allow remote code execution via crafted web content, prompting emergency patches."),
        story("Satellite Internet Expands Coverage Map Overnight",
              "A satellite internet operator expanded its coverage map overnight after bringing additional spacecraft online for previously waitlisted rural cells."),
        story("Esports League Confirms Season Schedule and Prize Pool",
              "An esports league confirmed its season schedule and an increased prize pool funded by new broadcast partners and franchise commitments."),
        story("Robotics Firm Ships Warehouse Pilot Fleet",
              "A robotics firm began shipping a pilot fleet of warehouse robots to logistics partners for live trials alongside human exception handling."),
        story("Developer Tools Update Speeds Local Build Times",
              "A popular developer tools suite released an update that significantly speeds local build times through smarter caching and parallel analysis."),
    ],
    "Entertainment": [
        story("Streaming Giant Greenlights Prestige Drama Series",
              "A streaming giant greenlit an eight-episode prestige drama that will film across three continents with a celebrated showrunner attached."),
        story("Arena Tour Dates Sell Out in Minutes",
              "Fans crashed ticketing apps as the first leg of a global arena tour went on sale, prompting promoters to add second nights in key cities."),
        story("Festival Line-Up Adds Surprise Headliner",
              "Organisers added a surprise headliner to a major festival bill days after the initial announcement, sparking a fresh wave of ticket sales."),
        story("Box Office Climbs on Franchise Sequel Opening",
              "A franchise sequel opened strongly at the global box office, led by family audiences and premium-format screens across major territories."),
        story("Award Season Contenders Gather for Industry Preview",
              "Award-season contenders gathered for an industry preview that mixed clips, panels, and informal networking ahead of voting windows."),
        story("Documentary Series Explores Music Scene Revival",
              "A documentary series exploring a regional music scene revival landed a prominent streaming slot after strong festival buzz."),
        story("Studio Confirms Spin-Off With Returning Cast",
              "A studio confirmed a spin-off series with several returning cast members from a hit ensemble drama, expanding secondary characters into leads."),
        story("Chart-Topping Album Returns for Anniversary Edition",
              "A chart-topping album returns as an anniversary edition with remastered tracks and previously unreleased demos for longtime fans."),
        story("Late-Night Host Announces Cross-Country Live Run",
              "A late-night host announced a cross-country live run featuring extended monologues and musical guests with lottery ticket access."),
        story("Critics Praise Breakout Performance in Indie Film",
              "Critics praised a breakout performance in a low-budget indie film that premiered to standing ovations at a boutique festival."),
    ],
}


def main() -> None:
    now = int(time.time())
    out = {
        "schemaVersion": 2,
        "generatedAtUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "seed_full_stories.py",
        "stats": {"feedsOk": 5, "feedsFailed": 0, "articleFetches": 50, "counts": {}},
        "BreakingNewsTab": [],
        "FinanceTab": [],
        "SportsTab": [],
        "TechnologyTab": [],
        "EntertainmentTab": [],
        "GeneralTab": [],
        "articles": [],
    }
    i = 0
    for tab, stories in TABS.items():
        arr = []
        for title, text in stories:
            i += 1
            body = text.strip()
            desc = " ".join(body.split())
            if len(desc) > 320:
                desc = desc[:317].rsplit(" ", 1)[0] + "..."
            arr.append(
                {
                    "title": title,
                    "text": body,
                    "description": desc,
                    "source_url": f"https://example.com/{tab.lower()}-{i}",
                    "category": tab,
                    "author": "SkunkNet Wire - sample",
                    "breaking": tab == "Breaking",
                    "publishedUnix": now - i * 400,
                    "source": "sample",
                }
            )
        out[tab] = arr
        out["stats"]["counts"][tab] = len(arr)

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    mins = {t: min(len(a["text"]) for a in out[t]) for t in TABS}
    print("wrote", OUT)
    print("counts", out["stats"]["counts"])
    print("min_chars", mins)


if __name__ == "__main__":
    main()
