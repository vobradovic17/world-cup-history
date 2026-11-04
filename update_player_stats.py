"""Add player World Cup totals and goalkeeper clean sheets from local matches."""

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
PROFILES_PATH = DATA / "world-cup-players-highlighted.json"
TEAM_ALIASES = {"West Germany": "Germany"}
PLACEMENT_RANK = {
    "Champion": 1,
    "Runner-up": 2,
    "Third place": 3,
    "Fourth place": 4,
    "Quarter-finals": 5,
    "Second round": 6,
    "Round of 16": 7,
    "Round of 32": 8,
    "Group stage": 9,
}

# Match files retain some source spellings and surname-first lineups.
ALIASES = {
    "Ademir de Menezes": ["ADEMIR"],
    "Carlos Alberto Torres": ["CARLOS ALBERTO"],
    "Dražan Jerković": ["Drazen JERKOVIC"],
    "Gerd Müller": ["Gerd MUELLER"],
    "Gianpiero Combi": ["Giampiero COMBI"],
    "Jürgen Klinsmann": ["Juergen KLINSMANN"],
    "Lothar Matthäus": ["Lothar MATTHAEUS"],
    "Manuel Neuer": ["NEUER Manuel"],
    "Thomas Müller": ["Thomas MUELLER", "MUELLER Thomas"],
    "Władysław Żmuda": ["Wladyslaw ZMUDA"],
}


def normalize(name):
    name = name.translate(str.maketrans({"ł": "l", "Ł": "L", "ø": "o", "Ø": "O"}))
    unaccented = "".join(
        character for character in unicodedata.normalize("NFKD", name.casefold())
        if not unicodedata.combining(character)
    )
    return re.sub(r"[^a-z0-9]", "", unaccented)


def main():
    profiles = json.loads(PROFILES_PATH.read_text())
    name_index = {}
    for profile in profiles:
        for spelling in [profile["name"], *ALIASES.get(profile["name"], [])]:
            key = normalize(spelling)
            if key in name_index and name_index[key] != profile["name"]:
                raise ValueError(f"Ambiguous player spelling: {spelling}")
            name_index[key] = profile["name"]

    matches = defaultdict(set)
    match_details = defaultdict(dict)
    tournaments = defaultdict(set)
    goals = defaultdict(int)
    clean_sheets = defaultdict(set)
    goalkeepers = set()
    for path in sorted(DATA.glob("world-cup-????-matches.json")):
        year = int(path.stem.split("-")[2])
        for match_number, match in enumerate(json.loads(path.read_text())["matches"]):
            match_id = (year, match_number)
            for side in ("home", "away"):
                team = match[f"{side}_team"]
                opponent_side = "away" if side == "home" else "home"
                participants = [(raw_name, True, None) for raw_name in match["lineup"][side]]
                participants.extend(
                    (sub["player_on"], False, sub["minute"])
                    for sub in match.get("substitutions", []) if sub["team"] == team
                )
                for raw_name, started, substitution_minute in participants:
                    name = name_index.get(normalize(raw_name))
                    if name:
                        matches[name].add(match_id)
                        tournaments[name].add((year, team))
                        detail = {
                            "year": year,
                            "date": match["date"],
                            "stage": match["stage"],
                            "home_team": match["home_team"],
                            "away_team": match["away_team"],
                            "score": match["score"],
                            "started": started,
                            "lineup": match["lineup"],
                            "substitutions": match["substitutions"],
                            "scorers": match["scorers"],
                        }
                        if not started:
                            detail["substitution_minute"] = substitution_minute
                        match_details[name].setdefault(match_id, detail)

                # The first starter is the goalkeeper. Follow any substitutions
                # for that position so a replacement is counted as well.
                active_goalkeeper = match["lineup"][side][0]
                match_goalkeepers = [active_goalkeeper]
                for sub in match.get("substitutions", []):
                    if sub["team"] == team and normalize(sub["player_off"]) == normalize(active_goalkeeper):
                        active_goalkeeper = sub["player_on"]
                        match_goalkeepers.append(active_goalkeeper)
                for raw_name in match_goalkeepers:
                    name = name_index.get(normalize(raw_name))
                    if name:
                        goalkeepers.add(name)
                        if match["score"][opponent_side] == 0:
                            clean_sheets[name].add(match_id)
            for scorer in match.get("scorers", []):
                if scorer.get("own_goal"):
                    continue
                name = name_index.get(normalize(scorer["player"]))
                if name:
                    goals[name] += 1

    for record in json.loads((DATA / "world-cup-most-appearances.json").read_text()):
        assert len(matches[record["name"]]) == record["matches"], record["name"]
    for record in json.loads((DATA / "world-cup-top-goalscorers.json").read_text()):
        assert goals[record["name"]] == record["goals"], record["name"]

    team_details = json.loads((DATA / "team-directory-details.json").read_text())
    placements = {
        team: {tournament["year"]: tournament["best_placement"] for tournament in details["tournaments"]}
        for team, details in team_details.items()
    }

    updated = []
    for profile in profiles:
        name = profile["name"]
        if len(match_details[name]) != len(matches[name]):
            raise ValueError(
                f"{name}: found {len(match_details[name])} match details "
                f"for {len(matches[name])} appearances"
            )
        years = {year for year, _ in matches[name]}
        finishes = [
            (year, placements[TEAM_ALIASES.get(team, team)][year])
            for year, team in tournaments[name]
        ]
        if finishes:
            best_rank = min(PLACEMENT_RANK[placement] for _, placement in finishes)
            best_placement = {
                "placement": next(placement for _, placement in finishes if PLACEMENT_RANK[placement] == best_rank),
                "years": sorted(year for year, placement in finishes if PLACEMENT_RANK[placement] == best_rank),
            }
        else:
            best_placement = None
        stats = {
            "name": name,
            "latest_highlight_year": profile["latest_highlight_year"],
            "world_cups_played": len(years),
            "matches_played": len(matches[name]),
            "matches": [match_details[name][match_id] for match_id in sorted(matches[name])],
            "goals_scored": goals[name],
            "best_placement": best_placement,
        }
        if name in goalkeepers:
            stats["clean_sheets"] = len(clean_sheets[name])
        stats.update({key: value for key, value in profile.items() if key not in stats and key != "clean_sheets"})
        updated.append(stats)

    PROFILES_PATH.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated player stats for {len(updated)} profiles")


if __name__ == "__main__":
    main()
