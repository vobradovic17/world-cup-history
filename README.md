# World Cup History Repo

This is a companion repo for the [worldcuphistory.com](https://worldcuphistory.com/) website.

## Tournament pages

Each edition has a standalone `tournament-YYYY.html` page. Match results, dates, and scores come from its file in `data/`. `data/tournament-editorial.json` holds the short editorial summaries and page facts; `data/tournament-page-stories.json` holds the five-paragraph narratives shown only on the tournament pages. The landing-page summaries remain in `script.js`. Run `python3 build_tournaments.py` after changing page data or stories to rebuild all pages. The 2030 file records an upcoming edition with no results.

The longer narratives were checked against [FIFA's history of champions from 1930 to 1978](https://www.fifa.com/en/tournaments/mens/worldcup/articles/world-cup-champions-1930-1978-uruguay-italy-germany-brazil-england-argentina), [the history from 1982 to 2026](https://www.fifa.com/en/tournaments/mens/worldcup/articles/world-cup-champions-1982-2026-italy-argentina-germany-brazil-france-spain), [the 2026 final report](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/spain-argentina-final-report-highlights), and [FIFA's 2030 hosting plan](https://inside.fifa.com/es/tournament-organisation/world-cup-2030). The match archive in this repository supports the scores and dates mentioned in them.

Each entry in `data/tournament-editorial.json` also records `topScorer` (goals and every player tied for the lead), `bestPlayer` (Golden Ball), `bestYoungPlayer`, and `bestGoalkeeper` (Yashin Award or Golden Glove). Young-player selections for 1958–2002 were made retrospectively and carry `selection: "retrospective"`; recipients from 2006 onward carry `selection: "official"`. `null` means the award was not presented for that edition, or that the 2030 tournament has not been played. Sources: FIFA's [top-scorer history](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/golden-boot-top-goalscorer), [Golden Ball winners](https://www.fifa.com/en/articles/rodri-earns-adidas-golden-ball), [complete Young Player history](https://www.fifa.com/es/articles/pau-cubarsi-premio-fifa-jugador-joven), and [Golden Glove winners](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/unai-simon-adidas-golden-glove).

Stadium details for 2018 and 2022 were matched to the [2018](https://fixturedownload.com/results/fifa-world-cup-2018) and [2022](https://fixturedownload.com/results/fifa-world-cup-2022) fixture lists. The 2026 host-stadium names follow [FIFA's venue list](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/fifa-world-cup-2026-hosts-cities-dates-usa-mexico-canada).

Every played match has `lineup.home` and `lineup.away` arrays of eleven starters, a `substitutions` array, and a `scorers` array. Substitutions record `team`, `player_on`, `player_off`, and `minute`; scorer records use `team`, `player`, and `minute`, with `penalty` or `own_goal` when applicable. Minutes are strings so added time can be represented as `90+3`. The 1930–1966 tournaments have no in-match substitutions. The 2030 file has no matches yet. Lineups, substitutions, and scorers through 2022 were checked against the public-domain [openfootball World Cup archive](https://github.com/openfootball/worldcup.json); each tournament JSON lists its source file. One incomplete source lineup in the 1954 Turkey–South Korea match uses the existing local eleven instead.

The tournament hero images in `assets/tournament-YYYY-hero.webp` are AI-generated illustrative reconstructions of specific editions. They are labelled as such on the pages and should not be presented as archival photographs.

The 1998 victory parade photograph is [“France 98 2” by Philippe Roos](https://commons.wikimedia.org/wiki/File:France_98_2_(32090133764).jpg), licensed under [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/). The original file is used unmodified; the page crops it to fit the image panel.

The 1962 World Cup photograph shows Garrincha and is from the [Arquivo Nacional collection](https://commons.wikimedia.org/wiki/File:Garrincha_na_copa_de_1962_(cropped).jpg), public domain.

The 2030 image is “FIFA World Cup Trophy photo” by Djuradj Vujcic, licensed under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/). The original file is used unmodified; the page crops it to fit the image panel. [Source](https://commons.wikimedia.org/wiki/File:FIFA_World_Cup_Trophy_photo_by_Djuradj_Vujcic.jpg).
