"""Build the static players page from the editorial data files."""

import html
import json
from pathlib import Path


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


def preview_person(name, team, extra="", prefix=""):
    flag = f'<img class="record-preview-flag" src="assets/team-flags/{TEAM_FLAGS[team]}.svg" alt="{esc(team)} flag" width="22" height="15">'
    suffix = f'<span>{esc(extra)}</span>' if extra else ""
    return f'<span class="record-preview-person">{esc(prefix)}{esc(name)}{flag}</span>{suffix}'


def featured_team(player):
    if player["awards"]:
        return player["awards"][0]["team"]
    if player["final_goals"]:
        return player["final_goals"][0]["team"]
    return player["world_cup_highlights"][0]["team"]


def record_list(records, number_key, unit):
    rows = []
    for record in records:
        name = record["name"]
        player_index = next((i for i, item in enumerate(PLAYERS, 1) if item["name"] == name), None)
        name_html = f'<a href="#player-{player_index}">{esc(name)}</a>' if player_index else esc(name)
        rows.append(
            f'<li><span class="record-rank">{record["rank"]:02d}</span>'
            f'<span class="record-person"><strong>{name_html}</strong>{record_flag(record["team"])}</span>'
            f'<span class="record-number" aria-label="{esc(record[number_key])} {unit}">{esc(record[number_key])}<small>{unit}</small></span></li>'
        )
    return "\n".join(rows)


PLAYER_INDEX = {player["name"]: index for index, player in enumerate(PLAYERS, 1)}


def record_person(name, team):
    if not name:
        return '<span class="record-person record-person-empty"><strong>Not awarded</strong></span>'
    index = PLAYER_INDEX.get(name)
    label = f'<a href="#player-{index}">{esc(name)}</a>' if index else esc(name)
    return f'<span class="record-person"><strong>{label}</strong>{record_flag(team)}</span>'


def tournament_record_list(records, kind):
    rows = []
    for record in reversed(records):
        if kind == "scorers":
            people = "".join(record_person(player["name"], player["team"]) for player in record["players"])
            meta = f'<span class="record-number" aria-label="{record["goals"]} goals">{record["goals"]}<small>goals</small></span>'
        else:
            field = "captain" if kind == "captains" else "coach" if kind == "coaches" else "name"
            people = record_person(record[field], record["team"])
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
            f'<li class="{row_class}"><span class="record-year">{record["year"]}</span>'
            f'<span class="record-people">{people}</span>{meta}</li>'
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


cards = []
for index, player in enumerate(PLAYERS, 1):
    paragraphs = [part.strip() for part in player["profile"].split("\n\n") if part.strip()]
    first = paragraphs[0] if paragraphs else ""
    rest = paragraphs[1:]
    team = featured_team(player)
    flag = f'<img class="player-flag" src="assets/team-flags/{TEAM_FLAGS[team]}.svg" alt="{esc(team)} flag" width="32" height="22">'
    photo = SOURCES.get(player["name"])
    image = esc(photo["file"]) if photo else "assets/player-portraits/fallback.svg"
    credit = CREDITS.get(player["name"], {})
    source_page = credit.get("file_page", photo["page"] if photo else "")
    photo_link = f'<a class="photo-source" href="{esc(source_page)}" target="_blank" rel="noopener noreferrer" aria-label="Image source for {esc(player["name"])}">Image source ↗</a>' if photo else ""
    more = ""
    if rest:
        extra = "".join(f'<p>{esc(part)}</p>' for part in rest)
        more = f'<details class="player-more"><summary><span class="more-closed">Read full profile</span><span class="more-open">Show less</span><span aria-hidden="true">↗</span></summary><div class="player-extra">{extra}</div></details>'
    cards.append(f'''<section class="player-card" id="player-{index}" aria-labelledby="player-title-{index}">
      <div class="player-image-wrap"><img src="{image}" alt="{esc(player['name'])}" loading="lazy" width="680" height="760">{photo_link}</div>
      <div class="player-copy">
        <h2 id="player-title-{index}">{esc(player['name'])} {flag}</h2>
        <p class="player-intro">{esc(first)}</p>
        {more}
      </div>
    </section>''')

credit_rows = []
for player in PLAYERS:
    credit = CREDITS.get(player["name"])
    if not credit:
        continue
    artist = credit["artist"] or "Creator listed on source page"
    license_name = credit["license"] or "See source page"
    credit_rows.append(f'<li><a href="{esc(credit["file_page"])}" target="_blank" rel="noopener noreferrer">{esc(player["name"])}</a><span>{esc(artist)} · {esc(license_name)}</span></li>')


page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0c354a">
  <meta name="description" content="Meet {len(PLAYERS)} players whose performances shaped World Cup history and explore records, awards, captains and coaches across the tournaments.">
  <title>Players | World Cup History</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="tournament.css">
  <link rel="stylesheet" href="players.css">
</head>
<body class="players-page">
  <a class="skip-link" href="#player-list">Skip to players</a>
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
      <div class="players-intro-note"><p>Explore each tournament's standout players, winning captains and coaches, all-time records, and profiles from across the eras.</p></div>
    </section>
    <div class="players-layout">
      <section class="player-records" aria-label="World Cup player records">
        {tournament_disclosures}
        <details class="record-disclosure" name="player-records">
          <summary><span class="record-row-inner"><span class="record-title">Top goalscorers <small>(All time)</small></span><span class="record-preview">{preview_person(SCORERS[0]['name'], SCORERS[0]['team'], f'· {SCORERS[0]["goals"]} goals')}</span><span class="record-count">{len(SCORERS)} players</span><span class="record-chevron" aria-hidden="true">⌄</span></span></summary>
          <div class="record-panel"><ol class="record-list">{record_list(SCORERS, 'goals', 'goals')}</ol></div>
        </details>
        <details class="record-disclosure" name="player-records">
          <summary><span class="record-row-inner"><span class="record-title">Most appearances</span><span class="record-preview">{preview_person(APPEARANCES[0]['name'], APPEARANCES[0]['team'], f'· {APPEARANCES[0]["matches"]} matches')}</span><span class="record-count">{len(APPEARANCES)} players</span><span class="record-chevron" aria-hidden="true">⌄</span></span></summary>
          <div class="record-panel"><ol class="record-list">{record_list(APPEARANCES, 'matches', 'matches')}</ol></div>
        </details>
        <details class="record-disclosure" name="player-records" id="prominent-players">
          <summary id="player-list"><span class="record-row-inner"><span class="record-title">Prominent players</span><span class="record-preview">{preview_person(PLAYERS[0]['name'], featured_team(PLAYERS[0]), prefix='From ')}{preview_person(PLAYERS[-1]['name'], featured_team(PLAYERS[-1]), prefix='to ')}</span><span class="record-count">{len(PLAYERS)} players</span><span class="record-chevron" aria-hidden="true">⌄</span></span></summary>
          <div class="players-main"><div class="player-list">{''.join(cards)}</div></div>
        </details>
      </section>
    </div>
    <details class="photo-credits"><summary>Photo credits <span aria-hidden="true">↗</span></summary><p>Select a name for its image source and usage details. Local images were converted to WebP for this page; some match photographs are served by their publishers.</p><ul>{''.join(credit_rows)}</ul></details>
  </main>
  <footer class="site-footer"><span>World Cup History © 2026</span><span>Made for the curious</span><a href="index.html#tournament-timeline">Explore tournaments ↑</a></footer>
  <script>
    function revealPlayerFromHash() {{
      if (!/^#player-[0-9]+$/.test(location.hash)) return;
      const player = document.getElementById(location.hash.slice(1));
      if (!player) return;
      document.getElementById('prominent-players').open = true;
      requestAnimationFrame(() => player.scrollIntoView());
    }}
    window.addEventListener('hashchange', revealPlayerFromHash);
    revealPlayerFromHash();
  </script>
</body>
</html>
'''
(ROOT / "players.html").write_text(page)
print(f"Built players.html with {len(PLAYERS)} profiles, {len(SCORERS)} scorers and {len(APPEARANCES)} appearance records")
