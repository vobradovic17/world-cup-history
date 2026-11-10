"""Build one static profile page for each highlighted World Cup figure."""

import html
import json
import re
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path

from update_player_stats import ALIASES, normalize
from site_paths import for_subdirectory_page


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
HERO_IMAGE = "assets/player-page-hero.webp"
FLAG_CODES = {
    "Argentina": "ar", "Belgium": "be", "Brazil": "br", "Bulgaria": "bg",
    "Chile": "cl", "Colombia": "co", "Croatia": "hr", "Czechoslovakia": "cz",
    "England": "gb-eng", "France": "fr", "Germany": "de", "Hungary": "hu",
    "Italy": "it", "Netherlands": "nl", "Peru": "pe", "Poland": "pl",
    "Portugal": "pt", "Russia": "ru", "Soviet Union": "soviet-union",
    "Spain": "es", "United States": "us", "Uruguay": "uy",
    "West Germany": "de", "Yugoslavia": "yugoslavia",
}
HOST_DISPLAY_NAMES = {
    1994: "USA",
    2002: "Korea + Japan",
    2026: "Canada · Mexico · USA",
}


def esc(value):
    return html.escape(str(value), quote=True)


def player_filename(name):
    plain = name.translate(str.maketrans({"ł": "l", "Ł": "L", "ø": "o", "Ø": "O"}))
    plain = "".join(char for char in unicodedata.normalize("NFKD", plain) if not unicodedata.combining(char))
    slug = re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")
    return f"{slug}.html"


def flag(team, class_name="player-flag", alt=""):
    code = FLAG_CODES.get(team)
    if not code:
        return ""
    return f'<img class="{class_name}" src="assets/team-flags/{code}.svg" alt="{esc(alt)}" width="28" height="19">'


def formatted_date(value):
    parsed = date.fromisoformat(value)
    return f"{parsed.day} {parsed:%b %Y}"


def player_side(match, spellings):
    sides = []
    for side in ("home", "away"):
        team = match[f"{side}_team"]
        participants = [*match["lineup"][side], *(
            sub["player_on"] for sub in match["substitutions"] if sub["team"] == team
        )]
        if any(normalize(raw) in spellings for raw in participants):
            sides.append(side)
    if len(sides) != 1:
        raise ValueError(f"Could not identify player team for {match['date']}: {match['home_team']}–{match['away_team']}")
    return sides[0]


def minute_key(value):
    base, _, added = str(value).partition("+")
    return int(base), int(added or 0)


def goal_list(match, side):
    team = match[f"{side}_team"]
    goals = sorted((goal for goal in match["scorers"] if goal["team"] == team), key=lambda goal: minute_key(goal["minute"]))
    if not goals:
        return ""
    items = []
    for goal in goals:
        note = " · own goal" if goal.get("own_goal") else " · pen." if goal.get("penalty") else ""
        items.append(f'<li><span>{esc(goal["player"])}</span><small>{esc(goal["minute"])}′{note}</small></li>')
    return f'<ul class="pm-goals">{"".join(items)}</ul>'


def team_sheet(match, side):
    team = match[f"{side}_team"]
    starters = "".join(f"<li>{esc(name)}</li>" for name in match["lineup"][side])
    subs = [sub for sub in match["substitutions"] if sub["team"] == team]
    changes = "".join(
        f'<li><span class="pm-change-minute">{esc(sub["minute"])}′</span>'
        f'<span><strong>{esc(sub["player_on"])}</strong> on · {esc(sub["player_off"])} off</span></li>'
        for sub in subs
    ) if subs else '<li class="pm-empty">No substitutions</li>'
    return f'''<section class="pm-team-sheet">
      <h5>{esc(team)}<span>{side}</span></h5>
      <h6>Starting lineup</h6><ul class="pm-starters">{starters}</ul>
      <h6>Substitutions</h6><ul class="pm-changes">{changes}</ul>
    </section>'''


def player_goal_count(match, player_team, spellings):
    return sum(
        1 for scorer in match["scorers"]
        if scorer["team"] == player_team
        and not scorer.get("own_goal")
        and normalize(scorer["player"]) in spellings
    )


def match_card(match, player_team, spellings=None, coach=False):
    home, away = match["home_team"], match["away_team"]
    score = match["score"]
    goals = player_goal_count(match, player_team, spellings) if spellings and not coach else 0
    multiplier = f'<span aria-hidden="true">× {goals}</span>' if goals > 1 else ""
    goal_badge = (
        f'<span class="pm-player-goals" role="img" aria-label="{goals} {"goal" if goals == 1 else "goals"} scored by this player">'
        f'<span class="pm-ball" aria-hidden="true">⚽</span>'
        f'{multiplier}</span>'
        if goals else ""
    )
    home_team = (
        f'<span class="pm-fixture-team{" is-player" if home == player_team else ""}">'
        f'<span class="pm-team-name">{esc(home)}</span>{goal_badge if home == player_team else ""}</span>'
    )
    away_team = (
        f'<span class="pm-fixture-team{" is-player" if away == player_team else ""}">'
        f'{goal_badge if away == player_team else ""}<span class="pm-team-name">{esc(away)}</span></span>'
    )
    fixture = (
        f'{home_team}<strong class="pm-score">{esc(score["home"])} '
        f'<span>:</span> {esc(score["away"])}</strong>{away_team}'
    )
    goal_sections = "".join(
        f'<section class="pm-goal-side" aria-label="Scorers for {esc(match[f"{side}_team"])}">'
        f'{goal_list(match, side)}</section>' for side in ("home", "away")
    )
    goal_grid = f'<div class="pm-goal-grid"><div class="pm-goal-sides">{goal_sections}</div></div>' if match["scorers"] else ""
    return f'''<details class="player-match">
      <summary><span class="pm-date"><time datetime="{esc(match['date'])}">{esc(formatted_date(match['date']))}</time><small>{esc(match['stage'])}</small></span>
      <span class="pm-fixture">{fixture}</span><span class="pm-open"><span aria-hidden="true">⌄</span></span></summary>
      <div class="pm-panel">{goal_grid}
      <div class="pm-lineups"><div class="pm-lineup-grid">{team_sheet(match, 'home')}{team_sheet(match, 'away')}</div></div></div>
    </details>'''


def campaigns_for_player(profile):
    spellings = {normalize(raw) for raw in [profile["name"], *ALIASES.get(profile["name"], [])]}
    campaigns = defaultdict(list)
    for match in profile["matches"]:
        side = player_side(match, spellings)
        campaigns[(match["year"], match[f"{side}_team"])].append(match)
    return {key: sorted(rows, key=lambda match: match["date"]) for key, rows in sorted(campaigns.items())}


def campaign_html(year, team, matches, placements, tournament_hosts, spellings=None, coach=False):
    placement = placements.get((year, team), "")
    goals = sum(player_goal_count(match, team, spellings) for match in matches) if spellings else 0
    count = len(matches)
    meta = f"{count} {'match' if count == 1 else 'matches'}"
    if not coach:
        meta += f" · {goals} {'goal' if goals == 1 else 'goals'}"
    rows = "".join(match_card(match, team, spellings, coach=coach) for match in matches)
    trophy = '<span class="pc-trophy" aria-hidden="true">🏆</span>' if placement == "Champion" else ""
    return f'''<details class="player-campaign">
      <summary><span class="pc-title"><span class="pc-year">{year}</span><span class="pc-country">{esc(tournament_hosts[year])}</span></span>
      <span class="pc-finish"><span class="pc-finish-text">{esc(placement)}</span>{flag(team, alt=team)}{trophy}</span>
      <span class="pc-meta">{meta}</span><span class="pc-chevron" aria-hidden="true"></span></summary>
      <div class="pc-matches">{rows}</div>
    </details>'''


def profile_page(profile, sources, credits, coach_wins, placements, tournament_matches, tournament_hosts):
    name = profile["name"]
    campaigns = campaigns_for_player(profile)
    coach = bool(coach_wins) and not campaigns
    if coach:
        for win in coach_wins:
            year, team = win["year"], win["team"]
            campaigns[(year, team)] = sorted(
                (match for match in tournament_matches[year] if team in (match["home_team"], match["away_team"])),
                key=lambda match: match["date"],
            )
    latest_team = list(campaigns)[-1][1] if campaigns else (profile["awards"][0]["team"] if profile["awards"] else "")
    source = sources.get(name)
    image_file = source["file"] if source else "assets/player-portraits/fallback.svg"
    image_alt = f"Portrait of {name}" if source else f"Illustrated placeholder for {name}"
    credit = credits.get(name)
    photo_credit = ""
    if source:
        credit_bits = []
        if credit:
            if credit.get("artist"):
                credit_bits.append(esc(credit["artist"]))
            if credit.get("license"):
                label = esc(credit["license"])
                credit_bits.append(
                    f'<a href="{esc(credit["license_url"])}" target="_blank" rel="noopener noreferrer">{label}</a>'
                    if credit.get("license_url") else label
                )
        details = f'<span>{" · ".join(credit_bits)}</span>' if credit_bits else ""
        photo_credit = (
            f'<div class="player-photo-credit"><a href="{esc(source["page"])}" target="_blank" rel="noopener noreferrer">Photo source ↗</a>{details}</div>'
        )
    paragraphs = "".join(f"<p>{esc(part.strip())}</p>" for part in profile["profile"].split("\n\n") if part.strip())
    if coach:
        stats = [("World Cup titles as coach", len(coach_wins)), ("Title-run matches", sum(map(len, campaigns.values())))]
    else:
        stats = [("World Cups", profile["world_cups_played"]), ("Matches", profile["matches_played"]), ("Goals", profile["goals_scored"])]
        if "clean_sheets" in profile:
            stats[-1] = ("Clean sheets", profile["clean_sheets"])
        if coach_wins:
            stats.append(("Titles as coach", len(coach_wins)))
    stats_html = "".join(f'<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>' for label, value in stats)
    placement = profile["best_placement"]
    if coach:
        success_heading_html = "<h3>World Cup titles as coach</h3>"
        placement_html = "".join(
            f'<dl class="player-placement"><dt>Title as coach</dt>'
            f'<dd>Champion · {win["year"]} · {esc(win["team"])} {flag(win["team"])}</dd></dl>'
            for win in coach_wins
        )
    else:
        success_heading_html = ""
        placement_html = (
            f'<dl class="player-placement"><dt>Best finish</dt>'
            f'<dd>{esc(placement["placement"])} · {", ".join(map(str, placement["years"]))}</dd></dl>'
            if placement else ""
        )
    awards_html = "".join(
        f'<li><span>{esc(award["award"])}</span><small>{award["year"]} · {esc(award["team"])}</small></li>'
        for award in profile["awards"]
    )
    honours = placement_html + (f'<ul class="player-awards">{awards_html}</ul>' if awards_html else "")
    if coach_wins and not coach:
        coach_titles = ", ".join(f"{win['year']} · {win['team']}" for win in coach_wins)
        honours += f'<p class="player-coach-honour"><strong>Champion as coach</strong><span>{esc(coach_titles)}</span></p>'
    spellings = {normalize(raw) for raw in [name, *ALIASES.get(name, [])]}
    campaign_rows = "".join(
        campaign_html(year, team, matches, placements, tournament_hosts, spellings, coach=coach)
        for (year, team), matches in sorted(campaigns.items())
    )
    campaign_title = "World Cup titles as coach" if coach else "World Cup campaigns"
    if not campaign_rows:
        campaign_rows = '<p class="player-no-matches">No World Cup playing appearances are recorded.</p>'
    coach_section = ""
    if coach_wins and not coach:
        coach_heading = "World Cup title as coach" if len(coach_wins) == 1 else "World Cup titles as coach"
        coach_description = "Explore the matches from the title run" if len(coach_wins) == 1 else "Explore the matches from each title run."
        title_runs = "".join(
            campaign_html(
                win["year"], win["team"],
                sorted((match for match in tournament_matches[win["year"]]
                        if win["team"] in (match["home_team"], match["away_team"])), key=lambda match: match["date"]),
                placements, tournament_hosts, coach=True,
            )
            for win in coach_wins
        )
        coach_section = f'''<section class="player-campaigns player-coach-runs" aria-labelledby="coach-runs-title">
        <div class="player-campaigns-heading"><div><p class="player-section-label">On the touchline</p><h2 id="coach-runs-title">{coach_heading}</h2></div>
        <p>{coach_description}</p></div>{title_runs}</section>'''
    role = "World Cup-winning coach" if coach else "World Cup player"
    success_html = (
        f'<aside class="player-success player-hero-success" aria-label="World Cup statistics and honours">'
        f'{success_heading_html}<dl class="player-stat-list">{stats_html}</dl>{honours}</aside>'
    )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0c354a">
  <meta name="description" content="{esc(name)} at the World Cup: statistics, honours, match results, lineups and scorers.">
  <title>{esc(name)} | World Cup History</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="tournament.css">
  <link rel="stylesheet" href="player-page.css">
</head>
<body class="player-page">
  <a class="skip-link" href="#player-profile">Skip to profile</a>
  <header class="site-header">
    <a class="wordmark" href="index.html#top" aria-label="World Cup History home"><span class="wordmark-mark" aria-hidden="true">◒</span><span>world cup<br><em>history</em></span></a>
    <nav class="site-nav" aria-label="Primary navigation"><a href="index.html">Tournaments</a><a href="teams.html">Teams</a><a class="is-current" aria-current="page" href="players.html">Players</a></nav>
  </header>
  <main>
    <section class="player-hero" aria-labelledby="page-title">
      <img class="player-hero-image" src="{HERO_IMAGE}" alt="" fetchpriority="high" width="1672" height="941">
      <div class="player-hero-shade"></div>
      <div class="player-hero-inner">
        <a class="player-back" href="players.html"><span aria-hidden="true">←</span> All players</a>
        <div class="player-hero-copy"><p class="player-eyebrow">{esc(role)}</p>
        <div class="player-hero-title-row"><h1 id="page-title">{esc(name)}</h1>
        <div class="player-hero-team">{flag(latest_team)} <span>{esc(latest_team)}</span></div></div>
        {success_html}</div>
        <p class="player-hero-credit">Illustrative football scene</p>
      </div>
    </section>
    <div class="player-page-wrap">
      <section class="player-profile" id="player-profile" aria-labelledby="profile-title">
        <div class="player-photo"><img src="{esc(image_file)}" alt="{esc(image_alt)}" loading="lazy" width="480" height="560">{photo_credit}</div>
        <div class="player-biography"><p class="player-section-label">The profile</p><h2 id="profile-title">{esc(name)}</h2>{paragraphs}</div>
      </section>
      <section class="player-campaigns" id="world-cups" aria-label="{esc(campaign_title)}">{campaign_rows}</section>
      {coach_section}
    </div>
  </main>
  <footer class="site-footer archive-footer"><span>World Cup History © 2026</span><span>Built with AI - Made for the curious</span><span>Get in touch - Comming soon</span></footer>
</body>
</html>
'''


def build_all_player_pages():
    profiles = json.loads((DATA / "world-cup-players-highlighted.json").read_text())
    sources = json.loads((ROOT / "assets/player-portraits/sources.json").read_text())
    credits = json.loads((ROOT / "assets/player-portraits/credits.json").read_text())
    coaches = json.loads((DATA / "world-cup-winning-coaches.json").read_text())
    team_details = json.loads((DATA / "team-directory-details.json").read_text())
    placements = {
        (entry["year"], team): entry["best_placement"]
        for team, details in team_details.items() for entry in details["tournaments"]
    }
    placements.update({(year, "West Germany"): value for (year, team), value in placements.items() if team == "Germany"})
    coach_wins = defaultdict(list)
    for row in coaches:
        if row["coach"]:
            coach_wins[row["coach"]].append(row)
    tournaments = {
        int(path.stem.split("-")[2]): json.loads(path.read_text())
        for path in DATA.glob("world-cup-????-matches.json")
    }
    tournament_matches = {year: data["matches"] for year, data in tournaments.items()}
    tournament_hosts = {
        year: HOST_DISPLAY_NAMES.get(year, data.get("host_country") or " · ".join(data["host_countries"]))
        for year, data in tournaments.items()
    }
    filenames = [player_filename(profile["name"]) for profile in profiles]
    if len(filenames) != len(set(filenames)):
        raise ValueError("Player filenames must be unique")
    for profile, filename in zip(profiles, filenames):
        (ROOT / "players" / filename).write_text(for_subdirectory_page(profile_page(profile, sources, credits, coach_wins[profile["name"]], placements, tournament_matches, tournament_hosts)))
    print(f"Built {len(profiles)} player profile pages")


if __name__ == "__main__":
    build_all_player_pages()
