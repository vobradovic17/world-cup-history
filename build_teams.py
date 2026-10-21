"""Build the ranked teams directory and its compact, on-demand detail data."""

from html import escape
import json
from pathlib import Path
import re
import unicodedata


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

# Historical sides use the flag they played under. The remaining values are
# filenames from the flag-icons collection copied into assets/team-flags.
FLAGS = {
    "Algeria": "dz", "Angola": "ao", "Argentina": "ar", "Australia": "au",
    "Austria": "at", "Belgium": "be", "Bolivia": "bo", "Bosnia and Herzegovina": "ba",
    "Brazil": "br", "Bulgaria": "bg", "Cameroon": "cm", "Canada": "ca",
    "Cape Verde": "cv", "Chile": "cl", "China": "cn", "Colombia": "co",
    "Costa Rica": "cr", "Croatia": "hr", "Cuba": "cu", "Curaçao": "cw",
    "Czech Republic": "cz", "Czechoslovakia": "cz", "Denmark": "dk", "DR Congo": "cd",
    "Dutch East Indies": "nl", "East Germany": "east-germany", "Ecuador": "ec",
    "Egypt": "eg", "El Salvador": "sv", "England": "gb-eng", "France": "fr",
    "Germany": "de", "Ghana": "gh", "Greece": "gr", "Haiti": "ht",
    "Honduras": "hn", "Hungary": "hu", "Iceland": "is", "Iran": "ir",
    "Iraq": "iq", "Israel": "il", "Italy": "it", "Ivory Coast": "ci",
    "Jamaica": "jm", "Japan": "jp", "Jordan": "jo", "Kuwait": "kw",
    "Mexico": "mx", "Morocco": "ma", "Netherlands": "nl", "New Zealand": "nz",
    "Nigeria": "ng", "North Korea": "kp", "Northern Ireland": "gb-nir",
    "Norway": "no", "Panama": "pa", "Paraguay": "py", "Peru": "pe",
    "Poland": "pl", "Portugal": "pt", "Qatar": "qa", "Republic of Ireland": "ie",
    "Romania": "ro", "Russia": "ru", "Saudi Arabia": "sa", "Scotland": "gb-sct",
    "Senegal": "sn", "Serbia": "rs", "Serbia and Montenegro": "serbia-montenegro",
    "Slovakia": "sk", "Slovenia": "si", "South Africa": "za", "South Korea": "kr",
    "Soviet Union": "soviet-union", "Spain": "es", "Sweden": "se",
    "Switzerland": "ch", "Togo": "tg", "Trinidad and Tobago": "tt",
    "Tunisia": "tn", "Turkey": "tr", "Ukraine": "ua",
    "United Arab Emirates": "ae", "United States": "us", "Uruguay": "uy",
    "Uzbekistan": "uz", "Wales": "gb-wls", "Yugoslavia": "yugoslavia",
    "Zaire": "zaire",
}

# These national teams use their flag as the badge in the team infobox.
FLAG_BADGE_TEAMS = {"Angola", "Bolivia", "Dutch East Indies", "Israel", "North Korea", "Serbia and Montenegro", "Togo"}


def slug(name: str) -> str:
    plain = "".join(character for character in unicodedata.normalize("NFKD", name) if not unicodedata.combining(character))
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")


def initials(name: str) -> str:
    words = [word for word in name.split() if word.lower() not in {"and", "of", "the"}]
    return "".join(word[0] for word in words[:2])


def build() -> None:
    rankings = json.loads((DATA / "world-cup-team-rankings.json").read_text())
    teams = {team["name"]: team for team in json.loads((DATA / "world-cup-teams.json").read_text())}
    hosts = {}
    for path in DATA.glob("world-cup-????-matches.json"):
        edition = json.loads(path.read_text())
        hosts[int(path.name[10:14])] = edition.get("host_country") or " · ".join(edition.get("host_countries", []))

    assert len(rankings) == len(teams) == len(FLAGS) == 89
    assert {entry["name"] for entry in rankings} == set(teams) == set(FLAGS)

    profiles = {}
    rows = []
    for entry in rankings:
        name = entry["name"]
        team = teams[name]
        rank = entry["rank"]
        best = entry["best_placement"]
        flag = f"assets/team-flags/{FLAGS[name]}.svg"
        crest_path = next((path for path in (
            ROOT / "assets" / "team-crests" / f"{slug(name)}.png",
            ROOT / "assets" / "team-crests" / f"{slug(name)}.svg",
        ) if path.exists()), None)
        crest = (
            {"kind": "image", "src": f"assets/team-crests/{crest_path.name}"}
            if crest_path else
            {"kind": "flag", "src": flag}
            if name in FLAG_BADGE_TEAMS else
            {"kind": "initials", "text": initials(name)}
        )
        years = " · ".join(
            f'<span class="team-year-with-trophy">{year}<span class="team-year-trophy" aria-hidden="true">🏆</span></span>'
            if best["placement"] == "Champion" else str(year)
            for year in best["years"]
        )
        count = best["count"]
        times = "time" if count == 1 else "times"
        placement_label = {
            "Champion": "Champions",
            "Runner-up": "Runners-up",
        }.get(best["placement"], best["placement"])
        rows.append(
            f'    <li class="team-item">\n'
            f'      <button class="team-row" type="button" id="team-toggle-{rank}" '
            f'aria-expanded="false" aria-controls="team-panel-{rank}" data-team="{escape(name, quote=True)}">'
            f'<span class="team-identity"><span class="team-name">{escape(name)}</span>'
            f'<img class="team-national-flag" src="{flag}" alt="" loading="lazy"></span>'
            f'<span class="team-finish">{escape(placement_label)} '
            f'<span class="team-finish-count" aria-label="{count} {times}">{count}×</span></span>'
            f'<span class="team-years">{years}</span>'
            f'<span class="team-chevron" aria-hidden="true">⌄</span></button>\n'
            f'      <div class="team-panel" id="team-panel-{rank}" role="region" '
            f'aria-labelledby="team-toggle-{rank}" hidden></div>\n'
            f'    </li>'
        )
        profiles[name] = {
            "name": name,
            "crest": crest,
            "best_placement": team["best_placement"],
            "totals": {key: team[key] for key in ("matches_played", "wins", "draws", "losses", "goals_for", "goals_against")},
            "tournaments": [
                {
                    **{key: tour[key] for key in ("year", "best_placement", "matches_played", "wins", "draws", "losses", "goals_for", "goals_against")},
                    "host": hosts[tour["year"]],
                    "matches": [
                        {key: match[key] for key in (
                            "date", "stage", "opponent", "score", "result",
                            "penalty_shootout", "home_away", "lineup", "substitutions", "scorers",
                        ) if key in match}
                        for match in tour["matches"]
                    ],
                }
                for tour in sorted(team["tournaments"], key=lambda tour: tour["year"])
            ],
        }

    page = ROOT / "teams.html"
    html = page.read_text()
    start = html.index('  <ol class="team-list team-list-unified"')
    end = html.index("</ol>", start) + len("</ol>")
    html = html[:start] + '  <ol class="team-list team-list-unified" aria-describedby="team-keyboard-help">\n' + "\n".join(rows) + "\n  </ol>" + html[end:]
    if 'id="team-keyboard-help"' not in html:
        html = html.replace('  <ol class="team-list team-list-unified"', '  <p class="visually-hidden" id="team-keyboard-help">Use the up and down arrow keys to move between teams. Press Enter or Space to open or close a team.</p>\n  <ol class="team-list team-list-unified"')
    if '<script src="teams.js" defer></script>' not in html:
        html = html.replace('  <link rel="stylesheet" href="teams.css">', '  <link rel="stylesheet" href="teams.css">\n  <script src="teams.js" defer></script>')
    page.write_text(html)
    serialized_profiles = json.dumps(profiles, ensure_ascii=False, separators=(",", ":"))
    (DATA / "team-directory-details.json").write_text(serialized_profiles + "\n")
    (DATA / "team-directory-details.js").write_text(
        "window.worldCupTeamProfiles = " + serialized_profiles + ";\n"
    )
    print(f"Built {len(rows)} team rows and detail profiles")


if __name__ == "__main__":
    build()
