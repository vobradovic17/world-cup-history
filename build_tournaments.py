"""Build standalone tournament pages from the archive match and editorial JSON."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from html import escape
import json
from pathlib import Path
import re

from build_teams import FLAGS as TEAM_FLAG_CODES


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
EDITORIAL = json.loads((DATA / "tournament-editorial.json").read_text())
YEARS = sorted(EDITORIAL)
PAGE_STORIES = json.loads((DATA / "tournament-page-stories.json").read_text())
assert set(PAGE_STORIES) == set(YEARS)
assert all(len(paragraphs) == 5 and all(paragraph.strip() for paragraph in paragraphs) for paragraphs in PAGE_STORIES.values())

# The team history file is the source for match lineups and substitutions.
# Player lists disambiguate matches that share a date, score, or historical team name.
TEAM_MATCH_DETAILS = {}
for team in json.loads((DATA / "world-cup-teams.json").read_text()):
    for tournament in team["tournaments"]:
        for match in tournament["matches"]:
            key = (
                tournament["year"], match["date"],
                tuple(match["lineup"]["home"]), tuple(match["lineup"]["away"]),
            )
            details = {field: match[field] for field in ("lineup", "substitutions")}
            if key in TEAM_MATCH_DETAILS:
                assert TEAM_MATCH_DETAILS[key] == details, key
            else:
                TEAM_MATCH_DETAILS[key] = details

WINNER_CANONICAL = {"West Germany": "Germany"}


def team_flag_markup(team: str) -> str:
    flag = TEAM_FLAG_CODES.get(WINNER_CANONICAL.get(team, team))
    return f'<img class="team-flag" src="assets/team-flags/{flag}.svg" alt="">' if flag else ""


def world_title_count(year: str, winner: str) -> int:
    canonical = WINNER_CANONICAL.get(winner, winner)
    return sum(
        1 for edition in YEARS
        if edition <= year
        and EDITORIAL[edition]["winner"] != "Future tournament"
        and WINNER_CANONICAL.get(EDITORIAL[edition]["winner"], EDITORIAL[edition]["winner"]) == canonical
    )


def champion_stamp(year: str, winner: str, is_future: bool) -> str:
    if is_future:
        return '<div class="winner-stamp"><span>Hosts</span><strong>Six host nations</strong><span>Across three continents</span></div>'
    count = world_title_count(year, winner)
    noun = "title" if count == 1 else "titles"
    trophies = "🏆" * count
    return (
        '<div class="winner-stamp"><span>World champions</span>'
        f'<span class="champion-trophies" role="img" aria-label="{h(winner)}: {count} World Cup {noun}">{trophies}</span>'
        f'<strong>{h(winner)} {team_flag_markup(winner)}</strong></div>'
    )


def tournament_text(year: str) -> str:
    host = "Centenary edition" if year == "2030" else EDITORIAL[year]["host"]
    return f"{year} {host}"


def h(value: object) -> str:
    return escape(str(value), quote=True)


def honor_stamp(label: str, players: list[dict], detail: str = "") -> str:
    if not players:
        return ""
    if len(players) == 1:
        player = players[0]
        context = " · Retrospective selection" if player.get("selection") == "retrospective" else ""
        subtitle = f'<span>{team_flag_markup(player["team"])}{h(player["team"] + context)}</span>'
        goals = f'<span>{h(detail)}</span>' if detail else ""
        return f'<div class="winner-stamp honor-stamp"><span>{h(label)}</span><strong>{h(player["name"])}</strong>{subtitle}{goals}</div>'
    people = ''.join(
        f'<div class="honor-person"><strong>{h(player["name"])}</strong><span>{team_flag_markup(player["team"])}{h(player["team"])}</span></div>'
        for player in players
    )
    return f'<div class="winner-stamp honor-stamp"><span>{h(label)}</span><div class="honor-people">{people}</div><span>{h(detail)} each</span></div>'


def short_date(value: str) -> str:
    d = date.fromisoformat(value)
    return f"{d.day} {d.strftime('%b %Y')}"


def date_span(matches: list[dict]) -> str:
    if not matches:
        return "Scheduled for 2030"
    first, last = min(date.fromisoformat(m["date"]) for m in matches), max(date.fromisoformat(m["date"]) for m in matches)
    if first.month == last.month:
        return f"{first.day}–{last.day} {last.strftime('%B %Y')}"
    return f"{first.day} {first.strftime('%B')} – {last.day} {last.strftime('%B %Y')}"


def stage_info(stage: str) -> tuple[int, str]:
    s = stage.lower()
    if s == "final":
        return 0, "Final"
    if "decisive match" in s:
        return 0, "Title-deciding match"
    if "third-place" in s:
        return 1, "Third-place match"
    if "semi" in s:
        return 2, "Semi-finals"
    if "quarter" in s:
        return 3, "Quarter-finals"
    if "round of 16" in s:
        return 4, "Round of 16"
    if "round of 32" in s:
        return 5, "Round of 32"
    if "final pool" in s:
        return 6, "Final pool"
    if "second-phase" in s:
        return 7, "Second round"
    return 8, "Group stage"


def result_note(match: dict) -> str:
    bits = []
    shootout = match.get("penalty_shootout")
    if shootout:
        if "winner" in shootout:
            bits.append(f"{shootout['winner']} won {shootout['score']} on penalties")
        else:
            home, away = shootout["home"], shootout["away"]
            winner = match["home_team"] if home > away else match["away_team"]
            bits.append(f"{winner} won {home}–{away} on penalties")
    elif match.get("extra_time"):
        bits.append("After extra time")
    if "replay" in match["stage"].lower():
        bits.append("Replay")
    return " · ".join(bits)


def group_name(stage: str, section: str) -> str | None:
    if section == "Group stage":
        found = re.match(r"Group ([A-Z])(?:\s|$)", stage)
    elif section == "Second round":
        found = re.match(r"Second-phase Group (\d+)(?:\s|$)", stage)
    else:
        return None
    return f"Group {found.group(1)}" if found else None


def group_sort_key(name: str) -> tuple[int, int | str]:
    suffix = name.split()[-1]
    return (0, int(suffix)) if suffix.isdigit() else (1, suffix)


def minute_sort_key(value: object) -> tuple[int, int]:
    minute, _, added = str(value).partition("+")
    return int(minute), int(added or 0)


def match_scorers(match: dict) -> str:
    scorers = match.get("scorers") or []
    if not scorers:
        return ""

    columns = []
    for side in ("home", "away"):
        team = match[f"{side}_team"]
        entries = []
        for scorer in sorted((s for s in scorers if s["team"] == team), key=lambda item: minute_sort_key(item["minute"])):
            detail = f"{scorer['minute']}′"
            if scorer.get("penalty"):
                detail += " pen."
            if scorer.get("own_goal"):
                detail += " own goal"
            entries.append(f"<li>{h(scorer['player'])} <span>{h(detail)}</span></li>")
        columns.append(f'<ul class="{side}-scorers" aria-label="Goals credited to {h(team)}">{"".join(entries)}</ul>')
    return f'<div class="match-scorers">{"".join(columns)}</div>'


def match_lineup(match: dict, year: str) -> str:
    key = (
        int(year), match["date"],
        tuple(match["lineup"]["home"]), tuple(match["lineup"]["away"]),
    )
    details = TEAM_MATCH_DETAILS[key]
    lineup = details["lineup"]
    available = {side: set(lineup[side]) for side in ("home", "away")}
    substitutions = {"home": [], "away": []}
    for substitution in details["substitutions"]:
        sides = [side for side in ("home", "away") if substitution["player_off"] in available[side]]
        if len(sides) != 1:
            raise ValueError(f"Cannot assign substitution in {year} {match['date']}: {substitution}")
        side = sides[0]
        substitutions[side].append(substitution)
        available[side].add(substitution["player_on"])

    columns = []
    for side in ("home", "away"):
        starters = "".join(f"<li>{h(player)}</li>" for player in lineup[side])
        changes = (
            '<ul class="match-lineup-substitutions">' + "".join(
                f'<li><span class="match-lineup-minute">{h(sub["minute"])}′</span>'
                f'<span><strong>{h(sub["player_on"])}</strong> on · {h(sub["player_off"])} off</span></li>'
                for sub in substitutions[side]
            ) + "</ul>"
            if substitutions[side] else '<p class="match-lineup-none">No substitutions</p>'
        )
        columns.append(
            f'<section class="match-lineup-side"><h4>{h(match[f"{side}_team"])}<span>{side.title()}</span></h4>'
            f'<h5>Starting lineup</h5><ul class="match-lineup-starters">{starters}</ul>'
            f'<h5>Substitutions</h5>{changes}</section>'
        )
    label = f"Details for {match['home_team']} versus {match['away_team']}"
    return (
        f'<details class="match-lineup"><summary aria-label="{h(label)}">Details</summary>'
        f'<div class="match-lineup-panel">{"".join(columns)}</div></details>'
    )


def match_row(match: dict, year: str, grouped: bool = False, final_venue: str = "") -> str:
    score = match["score"]
    venue = match.get("venue") or (final_venue if match["stage"] == "Final" else "")
    city = match.get("city") or ""
    venue_line = " · ".join(filter(None, [venue, city]))
    note = result_note(match)
    stage = match["stage"] if stage_info(match["stage"])[1] in {"Group stage", "Second round", "Final pool"} else ""
    if grouped:
        stage = "Playoff" if "playoff" in stage.lower() else ""
    description = f"{match['home_team']} {score['home']}, {match['away_team']} {score['away']}"
    context_parts = []
    if stage:
        context_parts.append(f"<span>{h(stage)}</span>")
    if note:
        context_parts.append(f'<span class="match-note">{h(note)}</span>')
    context_html = f'<div class="match-context">{"".join(context_parts)}</div>' if context_parts else ""
    return f'''<li class="match-row" aria-label="{h(description)}">
      <time class="match-date" datetime="{h(match['date'])}">{h(short_date(match['date']))}</time>
      <div class="match-body">
        {f'<div class="match-venue">{h(venue_line)}</div>' if venue_line else ''}
        <div class="match-fixture"><span class="match-team">{h(match['home_team'])}</span><span class="match-score">{h(score['home'])}<span aria-hidden="true"> : </span>{h(score['away'])}</span><span class="match-team away">{h(match['away_team'])}</span></div>
        {context_html}
        {match_scorers(match)}
      </div>
      {match_lineup(match, year)}
    </li>'''


def stage_rows(name: str, rows: list[dict], index: int, final_venue: str, year: str) -> str:
    if name not in {"Group stage", "Second round"}:
        return f'<ol class="match-list">{"".join(match_row(m, year, final_venue=final_venue) for m in rows)}</ol>'
    groups: dict[str, list[dict]] = defaultdict(list)
    for match in rows:
        group = group_name(match["stage"], name)
        if group is None:
            raise ValueError(f"Unexpected group stage: {match['stage']}")
        groups[group].append(match)
    sections = []
    for group in sorted(groups, key=group_sort_key):
        group_rows = groups[group]
        sections.append(f'''<section class="match-group" aria-labelledby="group-title-{index}-{group.split()[-1]}">
        <div class="group-heading"><h4 id="group-title-{index}-{group.split()[-1]}">{h(group)}</h4></div>
        <ol class="match-list">{''.join(match_row(m, year, grouped=True) for m in group_rows)}</ol>
      </section>''')
    return "".join(sections)


def build(year: str) -> None:
    editorial = EDITORIAL[year]
    archive = json.loads((DATA / f"world-cup-{year}-matches.json").read_text())
    matches = archive["matches"]
    assert len(matches) == archive["matches_played"], year
    teams = len({team for m in matches for team in (m["home_team"], m["away_team"])}) if matches else int(editorial["teams"])
    goals = sum(m["score"]["home"] + m["score"]["away"] for m in matches)
    final_label_parts = [part.strip() for part in editorial["finalLabel"].split("·")]
    final_venue = final_label_parts[1] if len(final_label_parts) > 1 and final_label_parts[0] in {"Final", "Decider"} else ""
    ordered = sorted(enumerate(matches), key=lambda item: (stage_info(item[1]["stage"])[0], date.fromisoformat(item[1]["date"]).toordinal(), item[0]))
    stages: dict[str, list[dict]] = {}
    for _, match in ordered:
        stages.setdefault(stage_info(match["stage"])[1], []).append(match)
    stage_nav = "".join(f'<a href="#stage-{i}">{h(name)}</a>' for i, (name, rows) in enumerate(stages.items()))
    sections = "".join(f'''<section class="match-stage" id="stage-{i}" aria-labelledby="stage-title-{i}">
      <div class="stage-heading"><h3 id="stage-title-{i}">{h(name)}</h3></div>
      {stage_rows(name, rows, i, final_venue, year)}
    </section>''' for i, (name, rows) in enumerate(stages.items()))
    if not sections:
        sections = '<section class="empty-state"><h3>Matches still to come</h3><p>The 2030 tournament has not been played. Results will be added when the matches take place.</p></section>'

    winner = editorial["winner"]
    is_future = not matches
    host = editorial["host"]
    hero_host = "Centenary edition" if is_future else host
    title = f"{year} World Cup in {host} | World Cup History"
    previous = YEARS[YEARS.index(year) - 1] if YEARS.index(year) else None
    following = YEARS[YEARS.index(year) + 1] if YEARS.index(year) < len(YEARS) - 1 else None
    previous_link = f'<a href="tournament-{previous}.html"><span aria-hidden="true">←</span> {previous}</a>' if previous else '<span></span>'
    following_link = f'<a href="tournament-{following}.html">{following} <span aria-hidden="true">→</span></a>' if following else '<span></span>'
    hero_all_link = f'<a class="hero-all" href="index.html#tournament-{year}" aria-label="All tournaments; return to {year} on the timeline"><span aria-hidden="true">←</span> All tournaments</a>'
    hero_previous_link = f'<a class="hero-previous" href="tournament-{previous}.html" aria-label="Previous tournament: {h(tournament_text(previous))}"><span aria-hidden="true">←</span> {h(tournament_text(previous))}</a>' if previous else ""
    hero_following_link = f'<a class="hero-next" href="tournament-{following}.html" aria-label="Next tournament: {h(tournament_text(following))}">{h(tournament_text(following))} <span aria-hidden="true">→</span></a>' if following else ""
    photo = f"assets/tournament-{year}-hero.webp" if not is_future else "assets/world-cup-trophy-2030.jpg"
    caption = f"Illustrative reconstruction of the {year} World Cup" if not is_future else "The World Cup trophy on display"
    hosts = ", ".join(archive.get("host_countries", [])) or archive.get("host_country", host)
    stats = [
        ("Host", hosts),
        ("Champion", winner if not is_future else "To be decided"),
        ("Dates", date_span(matches)),
        ("Planned teams" if is_future else "Teams", str(teams)),
        ("Matches played" if is_future else "Matches", str(len(matches))),
    ]
    if matches:
        stats.append(("Goals", str(goals)))
    stat_html = "".join(f"<div><dt>{h(label)}</dt><dd>{h(value)}</dd></div>" for label, value in stats)
    top_scorer = editorial["topScorer"]
    top_scorer_players = top_scorer["players"] if top_scorer else []
    honors = [
        ("Top scorers" if len(top_scorer_players) > 1 else "Top scorer", top_scorer_players, f'{top_scorer["goals"]} goals' if top_scorer else ""),
        ("Best player", [editorial["bestPlayer"]] if editorial["bestPlayer"] else [], ""),
        ("Best young player", [editorial["bestYoungPlayer"]] if editorial["bestYoungPlayer"] else [], ""),
        ("Best goalkeeper", [editorial["bestGoalkeeper"]] if editorial["bestGoalkeeper"] else [], ""),
    ]
    awards_html = ''.join(honor_stamp(label, players, detail) for label, players, detail in honors)
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0c354a">
  <meta name="description" content="{'Preview the 2030 World Cup centenary edition and its six host nations.' if is_future else f'Explore the {year} World Cup in {h(host)}: {h(winner)}, key moments and every match result.'}">
  <title>{h(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="tournament.css">
</head>
<body>
  <a class="skip-link" href="#story">Skip to tournament story</a>
  <header class="site-header">
    <a class="wordmark" href="index.html#top" aria-label="World Cup History home"><span class="wordmark-mark" aria-hidden="true">◒</span><span>world cup<br><em>history</em></span></a>
    <nav class="site-nav" aria-label="Primary navigation"><a class="is-current" href="index.html">Tournaments</a><a href="teams.html">Teams</a><a href="players.html">Players</a></nav>
  </header>
  <main>
    <section class="hero" aria-labelledby="page-title">
      <img class="hero-image" src="{h(photo)}" alt="" fetchpriority="high">
      <div class="hero-shade"></div>
      <div class="hero-inner"><nav class="hero-topline" aria-label="Tournament navigation">{hero_all_link}{hero_previous_link}{hero_following_link}</nav>
        <div class="hero-copy"><p class="eyebrow"><span class="eyebrow-line"></span> FIFA World Cup · {h(year)}</p><h1 id="page-title">{h(year)}<br><em class="{'long-host' if len(hero_host) > 12 else ''}">{h(hero_host)}</em></h1><p>{h(editorial['title'])} {h(editorial['titleAccent'])}</p></div>
        <div class="hero-bottom"><span>{h(caption)}</span></div>
      </div>
    </section>
    <div class="page-wrap">
      <section class="story" id="story" aria-labelledby="story-title"><div class="story-label"><span class="section-kicker">The tournament</span><span class="story-number">{h(year)}</span>
        {champion_stamp(year, winner, is_future)}
        {awards_html}</div>
        <div class="story-copy"><h2 id="story-title">{h(editorial['title'])}<br><em>{h(editorial['titleAccent'])}</em></h2>{''.join(f'<p>{h(paragraph)}</p>' for paragraph in PAGE_STORIES[year])}</div>
        <aside class="archive-aside" aria-label="Tournament summary and results navigation"><div class="aside-inner"><h2>{h(year)} in numbers</h2><dl class="summary-list">{stat_html}</dl>{f'<nav class="stage-nav" aria-label="Jump to match stage"><h3>Jump to a round</h3>{stage_nav}</nav>' if stages else ''}</div></aside>
      </section>
      <div class="archive-layout" id="matches">
        <div class="archive-main">{sections}</div>
      </div>
    </div>
  </main>
  <footer class="site-footer"><span>World Cup History © 2026</span><nav aria-label="Adjacent tournaments">{previous_link}{following_link}</nav><a href="index.html">Back to the archive ↑</a></footer>
</body>
</html>
'''
    (ROOT / f"tournament-{year}.html").write_text(html)


for edition in YEARS:
    build(edition)
print(f"Built {len(YEARS)} tournament pages")
