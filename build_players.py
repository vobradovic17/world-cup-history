"""Build the static players page from the editorial data files."""

import html
import json
from pathlib import Path
from build_player_pages import build_all_player_pages, player_filename


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
PLAYERS = json.loads((DATA / "world-cup-players-highlighted.json").read_text())
SCORERS = json.loads((DATA / "world-cup-top-goalscorers.json").read_text())
APPEARANCES = json.loads((DATA / "world-cup-most-appearances.json").read_text())
TOURNAMENT_SCORERS = json.loads((DATA / "world-cup-tournament-top-scorers.json").read_text())
BEST_PLAYERS = json.loads((DATA / "world-cup-tournament-best-players.json").read_text())
BEST_YOUNG_PLAYERS = json.loads((DATA / "world-cup-tournament-best-young-players.json").read_text())
BEST_GOALKEEPERS = json.loads((DATA / "world-cup-tournament-best-goalkeepers.json").read_text())
WINNING_CAPTAINS = json.loads((DATA / "world-cup-winning-captains.json").read_text())
WINNING_COACHES = json.loads((DATA / "world-cup-winning-coaches.json").read_text())
SOURCES_PATH = ROOT / "assets/player-portraits/sources.json"
SOURCES = json.loads(SOURCES_PATH.read_text()) if SOURCES_PATH.exists() else {}
CREDITS_PATH = ROOT / "assets/player-portraits/credits.json"
CREDITS = json.loads(CREDITS_PATH.read_text()) if CREDITS_PATH.exists() else {}
TEAM_FLAGS = {
    "Argentina": "ar", "Belgium": "be", "Brazil": "br", "Bulgaria": "bg",
    "Chile": "cl", "Colombia": "co", "Croatia": "hr", "Czechoslovakia": "cz",
    "England": "gb-eng", "France": "fr", "Germany": "de",
    "Hungary": "hu", "Italy": "it", "Netherlands": "nl", "Peru": "pe",
    "Poland": "pl", "Portugal": "pt", "Russia": "ru", "Soviet Union": "soviet-union",
    "Spain": "es", "United States": "us", "Uruguay": "uy", "West Germany": "de",
    "West Germany / Germany": "de", "Yugoslavia": "yugoslavia",
}

def esc(value):
    return html.escape(str(value), quote=True)


def record_flag(team):
    return f'<img class="record-flag" src="assets/team-flags/{TEAM_FLAGS[team]}.svg" alt="{esc(team)} flag" width="22" height="15">'


def preview_person(name, team, extra=""):
    flag = f'<img class="record-preview-flag" src="assets/team-flags/{TEAM_FLAGS[team]}.svg" alt="{esc(team)} flag" width="22" height="15">'
    suffix = f'<span>{esc(extra)}</span>' if extra else ""
    return f'<span class="record-preview-person">{esc(name)}{flag}</span>{suffix}'


PLAYER_BY_NAME = {player["name"]: player for player in PLAYERS}


def record_profiles(people):
    profiles = []
    for name, team in people:
        if not name:
            profiles.append('<div class="record-profile"><p>No player was selected for this edition.</p></div>')
            continue
        player = PLAYER_BY_NAME.get(name)
        if not player:
            raise ValueError(f"Missing record profile: {name}")
        photo = SOURCES.get(name)
        image_file = photo["file"] if photo else "assets/player-portraits/fallback.svg"
        image_alt = "" if photo else f"Illustrated placeholder for {name}"
        image = f'<img class="record-profile-image" src="{esc(image_file)}" alt="{esc(image_alt)}" loading="lazy" width="240" height="270">'
        source = f'<a class="record-profile-source" href="{esc(photo["page"])}" target="_blank" rel="noopener noreferrer">Image source ↗</a>' if photo else ""
        stats = [("World cups", player["world_cups_played"]), ("Matches", player["matches_played"])]
        if "clean_sheets" in player:
            stats.append(("Clean sheets", player["clean_sheets"]))
        else:
            stats.append(("Goals", player["goals_scored"]))
        stats_items = ''.join(f'<div><dt>{label}</dt><dd>{esc(value)}</dd></div>' for label, value in stats)
        stats_html = f'<dl class="record-profile-stats" aria-label="World Cup playing record">{stats_items}</dl>' if any(value for _, value in stats) else ''
        best_placement = player["best_placement"]
        if best_placement:
            years = ", ".join(str(year) for year in best_placement["years"])
            placement_tone = {
                "Champion": "gold",
                "Runner-up": "silver",
                "Third place": "bronze",
            }.get(best_placement["placement"])
            placement_class = "record-profile-award"
            if placement_tone:
                placement_class += f" record-profile-placement--{placement_tone}"
            placement = f'<span class="{placement_class}">{esc(best_placement["placement"])} · {esc(years)}</span>'
            placement_html = f'<div class="record-profile-awards record-profile-placement"><span class="record-profile-awards-label">Best placement</span><div class="record-profile-awards-list">{placement}</div></div>'
        else:
            placement_html = ''
        awards = ''.join(
            f'<span class="record-profile-award">{esc(award["award"])} · {award["year"]}'
            f'{" · retrospective" if award.get("selection") == "retrospective" else ""}</span>'
            for award in player["awards"]
        )
        awards_html = f'<div class="record-profile-awards"><span class="record-profile-awards-label">Awards</span><div class="record-profile-awards-list">{awards}</div></div>' if awards else ''
        profile_link = f'<a class="record-profile-link" href="{player_filename(name)}" aria-label="View {esc(name)} profile">View full profile <span aria-hidden="true">↗</span></a>'
        profiles.append(f'''<article class="record-profile"><div class="record-profile-media">{image}{source}</div><div class="record-profile-copy"><div class="record-profile-lead"><h3>{esc(name)} {record_flag(team)}</h3>{stats_html}</div><div class="record-profile-details">{awards_html}{placement_html}<div class="record-profile-text">{profile_link}</div></div></div></article>''')
    return f'<div class="record-entry-panel"><div class="record-profile-list">{"".join(profiles)}</div></div>'


def record_list(records, number_key, unit):
    rows = []
    for record in records:
        name = record["name"]
        name_html = esc(name)
        rows.append(
            f'<li class="record-item"><details class="record-entry" name="record-{number_key}">'
            f'<summary class="record-entry-heading"><span class="record-rank">{record["rank"]:02d}</span>'
            f'<span class="record-person"><strong>{name_html}</strong>{record_flag(record["team"])}</span>'
            f'<span class="record-entry-meta"><span class="record-number" aria-label="{esc(record[number_key])} {unit}">{esc(record[number_key])}<small>{unit}</small></span><span class="record-entry-chevron" aria-hidden="true">⌄</span></span></summary>'
            f'{record_profiles([(name, record["team"])])}</details></li>'
        )
    return "\n".join(rows)


def record_person(name, team):
    if not name:
        return '<span class="record-person record-person-empty"><strong>Not awarded</strong></span>'
    label = esc(name)
    return f'<span class="record-person"><strong>{label}</strong>{record_flag(team)}</span>'


def tournament_record_list(records, kind):
    rows = []
    for record in reversed(records):
        if kind == "scorers":
            people = "".join(record_person(player["name"], player["team"]) for player in record["players"])
            profile_people = [(player["name"], player["team"]) for player in record["players"]]
            meta = f'<span class="record-number" aria-label="{record["goals"]} goals">{record["goals"]}<small>goals</small></span>'
        else:
            field = "captain" if kind == "captains" else "coach" if kind == "coaches" else "name"
            people = record_person(record[field], record["team"])
            profile_people = [(record[field], record["team"])]
            if kind == "best_players":
                label = "Golden Ball" if record["selection"] == "golden_ball" else "Retrospective"
            elif kind == "young_players":
                label = "Official award" if record["selection"] == "official" else "Retrospective" if record["selection"] else ""
            elif kind == "goalkeepers":
                label = record["award"] or ""
            else:
                label = ""
            meta = f'<span class="record-edition-note">{esc(label)}</span>' if label else ""
        row_class = "record-edition-row" + (" record-edition-row--plain" if not meta else "")
        rows.append(
            f'<li class="record-item"><details class="record-entry" name="record-{kind}">'
            f'<summary class="record-entry-heading {row_class}"><span class="record-year">{record["year"]}</span>'
            f'<span class="record-people">{people}</span><span class="record-entry-meta">{meta}<span class="record-entry-chevron" aria-hidden="true">⌄</span></span></summary>'
            f'{record_profiles(profile_people)}</details></li>'
        )
    return "\n".join(rows)


def tournament_disclosure(title, records, kind):
    latest = records[-1]
    latest_name = latest["players"][0]["name"] if kind == "scorers" else latest.get("captain", latest.get("coach", latest.get("name")))
    latest_team = latest["players"][0]["team"] if kind == "scorers" else latest["team"]
    preview = preview_person(latest_name, latest_team)
    return f'''<details class="record-disclosure" name="player-records">
          <summary><span class="record-row-inner"><span class="record-title">{esc(title)}</span><span class="record-preview">{preview}</span><span class="record-count">{len(records)} editions</span><span class="record-chevron" aria-hidden="true">⌄</span></span></summary>
          <div class="record-panel"><ol class="record-list record-list-editions">{tournament_record_list(records, kind)}</ol></div>
        </details>'''


tournament_disclosures = "\n".join([
    tournament_disclosure("Top scorers", TOURNAMENT_SCORERS, "scorers"),
    tournament_disclosure("Best players", BEST_PLAYERS, "best_players"),
    tournament_disclosure("Best young players", BEST_YOUNG_PLAYERS, "young_players"),
    tournament_disclosure("Best goalkeepers", BEST_GOALKEEPERS, "goalkeepers"),
    tournament_disclosure("Winning captains", WINNING_CAPTAINS, "captains"),
    tournament_disclosure("Winning coaches", WINNING_COACHES, "coaches"),
])


credit_rows = []
for player in PLAYERS:
    credit = CREDITS.get(player["name"])
    if not credit:
        continue
    artist = credit["artist"] or "Creator listed on source page"
    license_name = credit["license"] or "See source page"
    license_url = credit.get("license_url")
    license_html = f'<a href="{esc(license_url)}" target="_blank" rel="noopener noreferrer">{esc(license_name)}</a>' if license_url else esc(license_name)
    credit_rows.append(f'<li><a href="{esc(credit["file_page"])}" target="_blank" rel="noopener noreferrer">{esc(player["name"])}</a><span>{esc(artist)} · {license_html}</span></li>')


page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0c354a">
  <meta name="description" content="Explore World Cup player records, awards, winning captains and coaches across the tournaments.">
  <title>Players | World Cup History</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="tournament.css">
  <link rel="stylesheet" href="players.css">
</head>
<body class="players-page">
  <a class="skip-link" href="#player-records">Skip to player records</a>
  <header class="site-header">
    <a class="wordmark" href="index.html#top" aria-label="World Cup History home"><span class="wordmark-mark" aria-hidden="true">◒</span><span>world cup<br><em>history</em></span></a>
    <nav class="site-nav" aria-label="Primary navigation"><a href="index.html">Tournaments</a><a href="teams.html">Teams</a><a class="is-current" aria-current="page" href="players.html">Players</a></nav>
  </header>
  <main>
    <section class="players-intro" aria-labelledby="page-title">
      <div class="players-intro-main">
        <p class="players-kicker"><span class="players-kicker-line" aria-hidden="true"></span><span>A century of football <span class="players-kicker-years">(1930 - 2030)</span></span></p>
        <h1 id="page-title">The players<br><em>across the eras.</em></h1>
      </div>
      <!-- <div class="players-intro-note"><p>Explore each tournament's standout players, winning captains and coaches, all-time records, and profiles from across the eras.</p></div> -->
      <div class="players-intro-note"><p>Explore each tournament's standout players, winning captains and coaches, and all-time records.</p></div>
    </section>
    <div class="players-layout">
      <section class="player-records" id="player-records" aria-label="World Cup player records">
        {tournament_disclosures}
        <details class="record-disclosure" name="player-records">
          <summary><span class="record-row-inner"><span class="record-title">Top goalscorers <small>(All time)</small></span><span class="record-preview">{preview_person(SCORERS[0]['name'], SCORERS[0]['team'], f'· {SCORERS[0]["goals"]} goals')}</span><span class="record-count">{len(SCORERS)} players</span><span class="record-chevron" aria-hidden="true">⌄</span></span></summary>
          <div class="record-panel"><ol class="record-list">{record_list(SCORERS, 'goals', 'goals')}</ol></div>
        </details>
        <details class="record-disclosure" name="player-records">
          <summary><span class="record-row-inner"><span class="record-title">Most appearances</span><span class="record-preview">{preview_person(APPEARANCES[0]['name'], APPEARANCES[0]['team'], f'· {APPEARANCES[0]["matches"]} matches')}</span><span class="record-count">{len(APPEARANCES)} players</span><span class="record-chevron" aria-hidden="true">⌄</span></span></summary>
          <div class="record-panel"><ol class="record-list">{record_list(APPEARANCES, 'matches', 'matches')}</ol></div>
        </details>
      </section>
    </div>
    <details class="photo-credits"><summary>Photo credits <span aria-hidden="true">↗</span></summary><p>Select a name for its image source and usage details. Local images were converted to WebP, and some were cropped; some match photographs are served by their publishers.</p><ul>{''.join(credit_rows)}</ul></details>
  </main>
  <footer class="site-footer archive-footer"><span>World Cup History © 2026</span><span>Built with AI - Made for the curious</span><span>Get in touch - Comming soon</span></footer>
</body>
</html>
'''
(ROOT / "players.html").write_text(page)
print(f"Built players.html with {len(PLAYERS)} profiles, {len(SCORERS)} scorers and {len(APPEARANCES)} appearance records")
build_all_player_pages()
