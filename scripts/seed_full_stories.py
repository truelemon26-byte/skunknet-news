#!/usr/bin/env python3
"""Seed skunknet_news.json with full multi-paragraph sample stories (no ads, no meta filler).

Each story is unique lead + topic-specific follow-up paragraphs. Do NOT inject SkunkNet
product copy about "full untruncated" publishing — the in-game reader strips that as junk.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "skunknet_news.json"


def story(title: str, paragraphs: list[str]) -> tuple[str, str]:
    body = "\n\n".join(p.strip() for p in paragraphs if p and p.strip())
    return title, body


TABS = {
    "Breaking": [
        story(
            "Island Alert: Global Markets Brace for Policy Shift",
            [
                "World leaders signal coordinated action as overnight market moves ripple through major exchanges. Analysts say the next forty-eight hours will set the tone for risk assets from equities to commodities.",
                "Treasury desks reported wider bid-ask spreads in early trading as funds repositioned ahead of expected policy statements from several major capitals.",
                "Commodity benchmarks moved in tandem with currency pairs linked to energy exporters, while equity futures oscillated between risk-on and defensive sessions.",
                "Officials cautioned that no final communique had been agreed, though working groups were scheduled to reconvene before markets open in Asia.",
            ],
        ),
        story(
            "Emergency Services Mobilise After Coastal Storm Surge",
            [
                "Coastal communities remain on high alert after overnight storm surges damaged harbour infrastructure and flooded low-lying roads. Authorities urged residents to avoid flooded routes while crews restore power.",
                "Rescue boats were deployed to several waterfront districts where vehicles were stranded and ground-floor businesses reported knee-deep water.",
                "Utility companies said substations near the shoreline were taken offline as a precaution, with portable generators prioritised for hospitals and shelters.",
                "Meteorologists warned that a secondary surge window remains possible if onshore winds strengthen again before the tide turns.",
            ],
        ),
        story(
            "Diplomatic Talks Resume After Overnight Escalation",
            [
                "Negotiators returned to the table after overnight clashes raised fears of a wider confrontation. Envoys pressed for an immediate de-escalation and a verified ceasefire corridor for civilians.",
                "Mediators said both sides had accepted a limited agenda focused on humanitarian access and a pause in heavy-weapons fire near population centres.",
                "Witnesses described intermittent shelling overnight before quiet returned around dawn, though verification teams had not yet reached all contested districts.",
                "Foreign ministries urged restraint and said further talks would depend on whether the ceasefire corridor can be monitored in real time.",
            ],
        ),
        story(
            "Major Airport Disruptions Follow System Outage",
            [
                "A cascading software failure grounded flights across several hubs for more than three hours, leaving thousands of passengers stranded as engineers restored core scheduling systems.",
                "Airlines diverted inbound aircraft where fuel and crew rules allowed, while departure boards showed cascading delays into the evening bank.",
                "Airport operators opened additional customer-service desks and distributed water and meal vouchers in terminals with the longest queues.",
                "Investigators said the outage began in a shared check-in platform and did not appear to involve a cyber intrusion, though a full audit is underway.",
            ],
        ),
        story(
            "Rescue Teams Reach Isolated Mountain Communities",
            [
                "Helicopter crews finally reached villages cut off by landslides after days of heavy rain. Medics treated injuries on site and evacuated critically ill patients to regional hospitals.",
                "Road crews continued clearing debris from the main valley highway, though engineers warned that unstable slopes could close the route again overnight.",
                "Local officials said temporary shelters had capacity for displaced families and that satellite phones were being distributed to community leaders.",
                "Weather models show a brief dry window that rescue coordinators hope to use for a second wave of supply drops.",
            ],
        ),
        story(
            "Government Issues Travel Advisory for Storm Corridor",
            [
                "Transport ministries issued a formal advisory covering coastal highways and ferry routes expected to face gale-force winds. Drivers were told to postpone non-essential journeys.",
                "Ferry operators cancelled several sailings and said refunds would be processed automatically for tickets booked within the advisory window.",
                "Highway patrols pre-positioned tow trucks at known flood points and asked motorists not to drive through standing water.",
                "Schools in the most exposed districts shifted to remote learning for the day as bus routes were suspended.",
            ],
        ),
        story(
            "Live Updates: Capital City Declares Temporary Curfew",
            [
                "City authorities declared a temporary overnight curfew after unrest damaged several commercial blocks. Police said the measure was designed to protect emergency workers and cleanup crews.",
                "Shop owners boarded windows along the main avenue while municipal teams cleared glass and burned debris from intersections.",
                "Transit agencies shortened evening service and advised passengers to complete journeys before the curfew start time.",
                "Officials said the order would be reviewed at dawn and lifted district by district if conditions remain calm.",
            ],
        ),
        story(
            "International Aid Flights Diverted to Regional Hub",
            [
                "Aid flights carrying medical kits and shelter materials were diverted to a regional hub after the primary runway was closed for repairs. Logistics teams reorganised last-mile distribution.",
                "Warehouse managers said cold-chain vaccines were prioritised for the first trucks leaving the alternate airport.",
                "Partner charities coordinated convoy schedules to avoid bottlenecks at border checkpoints that have slowed previous deliveries.",
                "Runway engineers estimated several days of work before the main airfield can resume heavy cargo operations.",
            ],
        ),
        story(
            "Power Grid Stabilises After Multi-State Blackout Scare",
            [
                "Grid operators restored normal frequency after a cascading fault briefly darkened parts of three states. Automatic protections isolated the fault before it could spread further.",
                "Hospitals reported seamless switchover to backup power, though some manufacturing plants lost a full production shift.",
                "Regulators opened an inquiry into whether maintenance schedules left insufficient reserve capacity during peak demand.",
                "Operators said additional spinning reserve would remain online through the weekend as a precaution.",
            ],
        ),
        story(
            "Security Sweep Clears Downtown After Suspicious Package",
            [
                "Bomb disposal teams cleared a busy downtown plaza after a suspicious package prompted an evacuation of nearby offices. The device was later declared a false alarm.",
                "Office workers waited in designated assembly areas while K-9 units and robots inspected the scene.",
                "Transit police briefly held trains under the plaza until the all-clear was issued mid-afternoon.",
                "City officials thanked the public for cooperating and said no further threat was identified.",
            ],
        ),
    ],
    "Business": [
        story(
            "Central Bank Holds Rates as Inflation Cools",
            [
                "Policymakers kept benchmark rates unchanged, citing cooler inflation prints and a desire to assess labour-market data before the next meeting.",
                "Bond yields eased modestly after the decision as traders reduced bets on an immediate further hike.",
                "Business groups welcomed the pause but said borrowing costs remain elevated for capital projects planned this year.",
                "The bank's statement left open the option of further tightening if services inflation re-accelerates.",
            ],
        ),
        story(
            "Tech Earnings Lift Equity Futures",
            [
                "Futures climbed after a cluster of technology firms beat revenue estimates, with chipmakers leading the advance on stronger AI spending guidance.",
                "Analysts highlighted rising data-centre capex as the main driver, though some cautioned that valuation multiples already price in aggressive growth.",
                "Semiconductor suppliers reported longer order backlogs for advanced packaging capacity.",
                "Broader indices followed the tech lead, with cyclical names lagging as investors rotated into growth.",
            ],
        ),
        story(
            "Oil Prices Slip on Inventory Surprise",
            [
                "Crude benchmarks slipped after weekly inventory data showed a larger-than-expected build at key hubs, while refining margins softened into the shoulder season.",
                "Traders said the build was concentrated in gasoline blendstocks rather than crude itself, tempering the sell-off.",
                "OPEC watchers noted that compliance with existing cuts remains uneven across members.",
                "Energy equities underperformed the wider market as the session closed.",
            ],
        ),
        story(
            "Retail Sales Beat Forecasts in Key Markets",
            [
                "Consumer spending surprised to the upside in several large economies, led by discretionary categories that had softened earlier in the year.",
                "Department-store chains reported stronger footfall over the holiday weekend, while online platforms cited higher average order values.",
                "Economists said real incomes have improved as inflation cooled, supporting household budgets.",
                "Retailers still warned that promotions remain necessary to clear seasonal inventory.",
            ],
        ),
        story(
            "Banking Sector Posts Stronger Loan Growth",
            [
                "Major lenders reported faster loan growth alongside stable deposit bases, easing concerns about funding stress as net interest margins held up.",
                "Commercial real-estate exposure remained a focus for investors, though charge-off rates stayed within guidance.",
                "Regulators said capital ratios across the peer group remain comfortably above minimums.",
                "Bank shares rose in early trading before giving back part of the gain into the close.",
            ],
        ),
        story(
            "Currency Markets Steady Ahead of Jobs Data",
            [
                "Foreign-exchange markets traded in tight ranges ahead of a pivotal employment report as speculators reduced leveraged positions.",
                "The dollar index hovered near recent averages while commodity currencies tracked overnight moves in metals.",
                "Options markets priced a modest post-data move, suggesting traders expect a contained reaction.",
                "Central-bank speakers are largely in blackout, leaving the jobs print as the week's main catalyst.",
            ],
        ),
        story(
            "Startup Funding Rebounds in Second Quarter",
            [
                "Venture funding rebounded from a multi-quarter trough as late-stage rounds returned and corporate venture arms re-engaged with AI infrastructure deals.",
                "Seed activity remained selective, with founders reporting longer diligence cycles and more milestone-based tranches.",
                "Secondary markets for private shares saw improved bid depth in a handful of well-known names.",
                "Limited partners said they are still pacing new commitments carefully after two years of slower distributions.",
            ],
        ),
        story(
            "Bond Yields Ease as Soft Landing Bets Rise",
            [
                "Government bond yields eased as investors leaned into soft-landing scenarios following cooler inflation and resilient growth data.",
                "Curve steepeners gained popularity among relative-value desks expecting policy easing later in the year.",
                "Corporate credit spreads tightened modestly, with investment-grade issuance calendars filling quickly.",
                "Strategists cautioned that a hot jobs print could reverse the move within a single session.",
            ],
        ),
        story(
            "Manufacturing PMI Edges Back Into Expansion",
            [
                "Factory surveys edged back above the expansion threshold as new orders stabilised and supplier delivery times normalised across key exporters.",
                "Input-price components cooled further, supporting the view that goods inflation pressure continues to fade.",
                "Employment sub-indices remained soft, suggesting firms are still cautious on hiring.",
                "Export-oriented economies led the improvement, while domestic-demand readings were mixed.",
            ],
        ),
        story(
            "Commodity Traders Watch Shipping Lane Delays",
            [
                "Commodity desks monitored delays along critical shipping lanes after weather and security incidents slowed transit times and lifted freight rates.",
                "Bulk carriers reported longer waits at chokepoints, adding days to typical voyage schedules.",
                "Insurance premia for certain corridors rose, feeding into landed costs for industrial metals and grains.",
                "Analysts said inventories at destination ports should buffer short disruptions, but prolonged delays would tighten nearby spreads.",
            ],
        ),
    ],
    "Sports": [
        story(
            "Derby Thriller Ends in Last-Minute Equaliser",
            [
                "A packed stadium erupted as the visitors snatched a point in stoppage time, keeping both sides in the title conversation after a scrambled corner.",
                "The home side had led for most of the second half following a deflected strike, only to concede from a late set piece.",
                "Managers on both benches praised the intensity but criticised defensive lapses in the final minutes.",
                "Bookmakers trimmed the gap between the rivals ahead of next weekend's fixtures.",
            ],
        ),
        story(
            "Grand Slam Favourite Advances in Straight Sets",
            [
                "The top seed needed just seventy-eight minutes to book a quarter-final berth, mixing heavy groundstrokes with clinical serving throughout.",
                "Unforced errors were kept to a minimum as the favourite dictated rallies from the baseline.",
                "The opponent struggled to hold serve after the first set and called for the trainer mid-match.",
                "Crowd interest now turns to a potential semi-final against a rising left-hander.",
            ],
        ),
        story(
            "Title Contenders Trade Blows in Night Fixture",
            [
                "Two championship contenders traded momentum swings in a night fixture that finished level after a breathless final quarter of play.",
                "Lead changes came in clusters as both offences found rhythm in transition.",
                "Defensive specialists on each roster logged heavy minutes and will be monitored for recovery ahead of a short turnaround.",
                "League standings remain tight at the top with less than a third of the season remaining.",
            ],
        ),
        story(
            "Transfer Window Buzz Intensifies Around Star Midfielder",
            [
                "Clubs across the top flight intensified interest in a creative midfielder entering the final year of a contract as valuations remain far apart.",
                "The player's representatives said no formal bids have been accepted, though talks with multiple suitors continue.",
                "Supporters groups urged the current club to open extension negotiations before the window closes.",
                "Analysts expect movement only if a release clause is triggered or a player-plus-cash structure emerges.",
            ],
        ),
        story(
            "Olympic Hopeful Breaks National Record in Trials",
            [
                "An Olympic hopeful shattered a long-standing national record at the selection trials, posting a time that would have medalled at the previous Games.",
                "Coaches said the performance caps a winter of altitude training and revised race pacing.",
                "Selection officials confirmed the athlete has met the automatic qualifying standard.",
                "Rivals congratulated the record-breaker while noting that championship rounds will demand another step up.",
            ],
        ),
        story(
            "Coach Praises Squad Depth After Away Win",
            [
                "A visiting coach praised squad depth after rotation players delivered a controlled away win against a direct rival in the standings.",
                "Two academy graduates started and contributed to the first goal with a sharp combination on the right flank.",
                "The hosts struggled to create clear chances after an early red card changed the tactical balance.",
                "Fixture congestion means further rotation is likely before the midweek cup tie.",
            ],
        ),
        story(
            "Injury Update Clouds Weekend Line-Up Plans",
            [
                "Medical staff provided a cautious update on two first-team regulars nursing soft-tissue injuries ahead of a pivotal weekend fixture.",
                "One midfielder is expected to train fully by Friday, while a full-back remains doubtful.",
                "The coaching staff has called up a reserve defender as cover and may reshuffle the back line.",
                "Fans were told ticket holders should check team news closer to kick-off for confirmed absences.",
            ],
        ),
        story(
            "Underdogs Stun League Leaders in Cup Upset",
            [
                "Lower-league underdogs produced a famous cup upset, eliminating the league leaders with a late counterattack and composed finish.",
                "The visitors defended deep for long spells and struck when a misplaced pass opened the pitch.",
                "Celebrations spilled onto the pitch after the final whistle as travelling supporters sang through the night.",
                "The defeated side's manager accepted responsibility and said focus must return immediately to league form.",
            ],
        ),
        story(
            "Marathon Course Record Falls in City Race",
            [
                "A city marathon record fell as elite fields benefited from cool temperatures and a revised, faster course through the downtown loop.",
                "Pacemakers held a disciplined tempo through the halfway mark before the leaders broke clear.",
                "Charity runners praised organisation at water stations despite record participation numbers.",
                "Organisers said they will review road-closure timings after some residential complaints about access.",
            ],
        ),
        story(
            "Broadcast Deal Extends Live Coverage Package",
            [
                "A multi-year broadcast deal extended live coverage packages for domestic leagues and cup competitions with upgraded camera technology.",
                "Rights holders promised more multi-angle replays and expanded commentary teams for midweek fixtures.",
                "Clubs will share incremental revenue under a formula weighted toward competitive balance.",
                "Fans will see the new production package begin with the opening weekend of the next campaign.",
            ],
        ),
    ],
    "Gaming_Tech": [
        story(
            "Chipmaker Unveils Next-Gen AI Accelerator",
            [
                "A leading chipmaker unveiled its next-generation AI accelerator, claiming doubled inference throughput for large language models while cutting rack power draw.",
                "Early access partners said software stacks will need updates to exploit new memory interconnects.",
                "Cloud providers are expected to announce instance types once volume production ramps later this year.",
                "Competitors responded with roadmap teasers but did not match the published performance claims.",
            ],
        ),
        story(
            "Studio Delays Flagship Title to Polish Multiplayer",
            [
                "A major studio delayed its flagship title by six weeks to polish multiplayer stability after internal playtests exposed matchmaking edge cases.",
                "Single-player campaign content is described as feature-complete, with the extra time focused on netcode and anti-cheat.",
                "Pre-order bonuses will remain valid through the new launch window, the publisher said.",
                "Community managers asked players to treat leaked build footage as outdated.",
            ],
        ),
        story(
            "Open-Source Model Tops Independent Benchmark Suite",
            [
                "An open-source language model topped an independent benchmark suite covering reasoning, coding, and multilingual tasks after denser data curation.",
                "Researchers credited improved filtering of low-quality web text and a longer context window.",
                "Enterprise adopters said they are evaluating the model for on-prem deployments where data residency matters.",
                "Benchmark organisers cautioned that real-world product quality still depends on fine-tuning and safety layers.",
            ],
        ),
        story(
            "Cloud Provider Cuts Inference Pricing for Startups",
            [
                "A major cloud provider cut inference pricing for early-stage startups, aiming to lower barriers for product experimentation on GPU capacity.",
                "Credits will stack with existing startup programmes for the first twelve months of usage.",
                "Analysts said the move intensifies competition among hyperscalers for AI-native customers.",
                "Startups still face queue times for the highest-end accelerators during peak demand windows.",
            ],
        ),
        story(
            "Handheld Console Firmware Adds Performance Mode",
            [
                "Handheld console makers shipped a firmware update adding a performance mode that raises frame-rate targets for select demanding titles.",
                "Battery life decreases in the new mode, and thermal limits may still throttle during long sessions.",
                "Players reported smoother gameplay in several third-party ports after installing the patch.",
                "A further update is planned to expand the title whitelist based on community feedback.",
            ],
        ),
        story(
            "Security Researchers Flag Critical Browser Flaw",
            [
                "Security researchers disclosed a critical browser flaw that could allow remote code execution via crafted web content, prompting emergency patches.",
                "Vendors urged users to update immediately and temporarily disable risky extensions until patches propagate.",
                "No confirmed mass exploitation was reported at disclosure time, though proof-of-concept code circulated among researchers.",
                "Enterprise IT teams were advised to push updates through managed channels within twenty-four hours.",
            ],
        ),
        story(
            "Satellite Internet Expands Coverage Map Overnight",
            [
                "A satellite internet operator expanded its coverage map overnight after bringing additional spacecraft online for previously waitlisted rural cells.",
                "Early customers in newly unlocked regions reported download speeds consistent with neighbouring cells.",
                "Installation kits remain back-ordered in some markets as demand surged after the map update.",
                "Regulators continue to review spectrum coordination requests for further constellation growth.",
            ],
        ),
        story(
            "Esports League Confirms Season Schedule and Prize Pool",
            [
                "An esports league confirmed its season schedule and an increased prize pool funded by new broadcast partners and franchise commitments.",
                "Regular-season matches will air on expanded streaming windows with mid-week show matches.",
                "Franchises must finalise rosters before a hard lock date to remain eligible for playoffs.",
                "Viewership targets were raised after last season's finals set a series record.",
            ],
        ),
        story(
            "Robotics Firm Ships Warehouse Pilot Fleet",
            [
                "A robotics firm began shipping a pilot fleet of warehouse robots to logistics partners for live trials alongside human exception handling.",
                "The robots focus on repetitive tote moves while staff handle irregular parcels and quality checks.",
                "Early sites will measure pick rates, downtime, and safety incidents over a ninety-day window.",
                "Unions at some facilities said they want clearer retraining commitments before wider rollout.",
            ],
        ),
        story(
            "Developer Tools Update Speeds Local Build Times",
            [
                "A popular developer tools suite released an update that significantly speeds local build times through smarter caching and parallel analysis.",
                "Benchmarks from maintainers showed double-digit percentage gains on medium-sized monorepos.",
                "The update also tightens default security scanning for dependency advisories.",
                "Teams were advised to clear old cache directories once after upgrading to avoid stale artefacts.",
            ],
        ),
    ],
    "Entertainment": [
        story(
            "Streaming Giant Greenlights Prestige Drama Series",
            [
                "A streaming giant greenlit an eight-episode prestige drama that will film across three continents with a celebrated showrunner attached.",
                "Casting notices have gone out for two lead roles, with supporting parts expected to be filled from local talent pools.",
                "The series is eyed for a late-next-year premiere window pending post-production schedules.",
                "Industry buyers said the project was among the most competitive pitches of the season.",
            ],
        ),
        story(
            "Arena Tour Dates Sell Out in Minutes",
            [
                "Fans crashed ticketing apps as the first leg of a global arena tour went on sale, prompting promoters to add second nights in key cities.",
                "Dynamic pricing drew criticism from fan groups even as primary inventory vanished within minutes.",
                "The artist posted a thank-you message and promised more dates would be announced soon.",
                "Secondary markets saw immediate markups, triggering warnings about counterfeit listings.",
            ],
        ),
        story(
            "Festival Line-Up Adds Surprise Headliner",
            [
                "Organisers added a surprise headliner to a major festival bill days after the initial announcement, sparking a fresh wave of ticket sales.",
                "The late addition fills a Saturday night slot that had been listed as to-be-announced.",
                "Camping packages for the weekend sold out shortly after the update went live.",
                "Local councils confirmed additional transit services for the peak arrival evening.",
            ],
        ),
        story(
            "Box Office Climbs on Franchise Sequel Opening",
            [
                "A franchise sequel opened strongly at the global box office, led by family audiences and premium-format screens across major territories.",
                "Critics were mixed, but audience scores remained solid through the opening weekend.",
                "Studio executives said international markets outperformed domestic tallies for the first time in the series.",
                "A spin-off is already in early development pending final weekend holds.",
            ],
        ),
        story(
            "Award Season Contenders Gather for Industry Preview",
            [
                "Award-season contenders gathered for an industry preview that mixed clips, panels, and informal networking ahead of voting windows.",
                "Publicists emphasised craft categories as much as lead performances in this year's campaigns.",
                "Several films still lack wide release dates, keeping strategists flexible on qualifying runs.",
                "Voters said the field feels unusually deep in documentary and international features.",
            ],
        ),
        story(
            "Documentary Series Explores Music Scene Revival",
            [
                "A documentary series exploring a regional music scene revival landed a prominent streaming slot after strong festival buzz.",
                "Directors spent two years filming clubs, studios, and community radio stations that nurtured new acts.",
                "Soundtrack rights clearances delayed the premiere but added rare archival performances.",
                "Local musicians said the series has already driven ticket sales for upcoming shows.",
            ],
        ),
        story(
            "Studio Confirms Spin-Off With Returning Cast",
            [
                "A studio confirmed a spin-off series with several returning cast members from a hit ensemble drama, expanding secondary characters into leads.",
                "Writers' rooms are already outlining a first season that bridges directly from the parent show's finale.",
                "Fans reacted warmly online, though some worried about overextending the franchise.",
                "Production is expected to begin early next year on familiar soundstages.",
            ],
        ),
        story(
            "Chart-Topping Album Returns for Anniversary Edition",
            [
                "A chart-topping album returns as an anniversary edition with remastered tracks and previously unreleased demos for longtime fans.",
                "Listening parties are planned in several cities, with limited vinyl variants for collectors.",
                "Critics who revisited the record praised the remaster's clearer low end and restored dynamics.",
                "The artist said proceeds from a special bundle will support music education charities.",
            ],
        ),
        story(
            "Late-Night Host Announces Cross-Country Live Run",
            [
                "A late-night host announced a cross-country live run featuring extended monologues and musical guests with lottery ticket access.",
                "Television tapings will pause for two weeks while the tour visits mid-size arenas.",
                "Guest bookings already include comedians and bands tied to the show's recent viral segments.",
                "Local promoters said demand forced an extra matinee in one coastal market.",
            ],
        ),
        story(
            "Critics Praise Breakout Performance in Indie Film",
            [
                "Critics praised a breakout performance in a low-budget indie film that premiered to standing ovations at a boutique festival.",
                "The lead actor had mostly television credits before taking the role on a compressed shoot.",
                "Distributors are bidding for rights after midnight screenings sold out three nights running.",
                "The director said a wider release strategy will prioritise community cinemas before streaming.",
            ],
        ),
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
