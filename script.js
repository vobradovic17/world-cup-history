const tournamentData = [
  ['1930', 'Uruguay', '🇺🇾', 'Uruguay', '13', '18', 'The beginning', 'of everything.', 'The inaugural FIFA World Cup was held in Uruguay in 1930. Thirteen teams came to Montevideo for the tournament, shaped by long sea journeys, crowded terraces and the excitement of a football world meeting for the first time. Uruguay, the reigning Olympic champions and hosts, reached the final against Argentina at the newly opened Estadio Centenario. After falling behind, La Celeste turned the match around to win 4–2, becoming the first nation to lift the Jules Rimet Trophy.', 'URU', '4', '2', 'ARG', 'Montevideo, Uruguay', 'Final · Estadio Centenario'],
  ['1934', 'Italy', '🇮🇹', 'Italy', '16', '17', 'The first home crown', 'sets the tone.', 'Italy hosted the second FIFA World Cup, the first edition to use a qualification phase and a straight knockout format. Sixteen teams travelled to Italy. In the final at Rome’s Stadio Nazionale PNF, Czechoslovakia took the lead before Raimundo Orsi equalised and Angelo Schiavio scored in extra time to give Italy a 2–1 victory and its first world title.', 'ITA', '2', '1', 'TCH', 'Rome, Italy', 'Final · Stadio Nazionale PNF'],
  ['1938', 'France', '🇮🇹', 'Italy', '15', '18', 'A title defended', 'away from home.', 'France hosted the third FIFA World Cup, a compact knockout tournament played across ten venues. Fifteen teams took part after Austria withdrew, and Italy arrived as the reigning champion. In the final at Paris’s Stade Olympique de Colombes, Italy defeated Hungary 4–2, with doubles from Gino Colaussi and Silvio Piola, becoming the first nation to retain the trophy.', 'ITA', '4', '2', 'HUN', 'Paris, France', 'Final · Stade Olympique de Colombes'],
  ['1950', 'Brazil', '🇺🇾', 'Uruguay', '13', '22', 'The match', 'that echoed.', 'Brazil hosted the fourth FIFA World Cup, whose unusual final stage was decided by a round-robin group rather than a single final. Uruguay, Brazil, Sweden and Spain competed for the title, but Brazil arrived at the decisive match as the overwhelming favourite after two big wins. Before a huge Maracanã crowd, Uruguay came from behind to win 2–1 through goals by Juan Alberto Schiaffino and Alcides Ghiggia, creating the shock remembered as the Maracanazo.', 'URU', '2', '1', 'BRA', 'Rio de Janeiro, Brazil', 'Decider · Estádio do Maracanã'],
  ['1954', 'Switzerland', '🇩🇪', 'West Germany', '16', '26', 'A comeback', 'for the ages.', 'Switzerland hosted the fifth FIFA World Cup, a fast and high-scoring tournament remembered for the meeting of West Germany and Hungary’s celebrated Golden Team. Hungary had already beaten the Germans 8–3 in the group stage, and then raced into a 2–0 lead in the rain-soaked final at Bern’s Wankdorf Stadium. Max Morlock and Helmut Rahn levelled the match before Rahn struck again late to complete the 3–2 Miracle of Bern.', 'FRG', '3', '2', 'HUN', 'Bern, Switzerland', 'Final · Wankdorf Stadium'],
  ['1958', 'Sweden', '🇧🇷', 'Brazil', '16', '35', 'A star', 'arrives.', 'Sweden hosted the sixth FIFA World Cup, where Brazil’s fluid attacking football finally produced its first world title. A 17-year-old Pelé emerged as the tournament’s defining figure, scoring six goals after entering the knockout stage. In the final at Stockholm’s Råsunda Stadium, Brazil recovered from an early Swedish lead to win 5–2, with Pelé scoring twice and Vavá also claiming a brace.', 'BRA', '5', '2', 'SWE', 'Stockholm, Sweden', 'Final · Råsunda Stadium'],
  ['1962', 'Chile', '🇧🇷', 'Brazil', '16', '32', 'The champions', 'hold on.', 'Chile hosted the seventh FIFA World Cup, a hard-fought tournament shaped by injuries, intense defending and the brilliance of Brazil’s attacking core. Pelé was sidelined early, but Garrincha and Amarildo helped carry the champions through the knockout stage. In the final at Santiago’s Estadio Nacional, Czechoslovakia scored first before Amarildo, Zito and Vavá turned the match around for a 3–1 victory and Brazil’s second consecutive title.', 'BRA', '3', '1', 'TCH', 'Santiago, Chile', 'Final · Estadio Nacional'],
  ['1966', 'England', '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'England', '16', '32', 'Football comes', 'home.', 'England hosted the eighth FIFA World Cup, a tournament defined by Alf Ramsey’s disciplined team and a final that still divides opinion. At Wembley, West Germany scored early before Geoff Hurst equalised, Martin Peters put England ahead and Wolfgang Weber forced extra time. Hurst then completed the first hat-trick in a World Cup final, including the famous disputed third goal, to seal a 4–2 victory and England’s only world title.', 'ENG', '4', '2', 'FRG', 'London, England', 'Final · Wembley Stadium'],
  ['1970', 'Mexico', '🇧🇷', 'Brazil', '16', '32', 'The beautiful game', 'in full colour.', 'Mexico hosted the ninth FIFA World Cup, the first played at altitude and the first to be broadcast widely in colour. Brazil arrived with a remarkable attacking side built around Pelé, Jairzinho, Tostão, Gérson and Rivellino, then swept through the tournament with a style that made the competition feel electric. In the final at Mexico City’s Estadio Azteca, Pelé opened the scoring and Carlos Alberto finished a flowing move as Brazil defeated Italy 4–1 to claim a third title and keep the Jules Rimet Trophy permanently.', 'BRA', '4', '1', 'ITA', 'Mexico City, Mexico', 'Final · Estadio Azteca'],
  ['1974', 'West Germany', '🇩🇪', 'West Germany', '16', '38', 'A final', 'turned around.', 'West Germany hosted the tenth FIFA World Cup, a tournament remembered for the Netherlands’ expressive total football and the hosts’ composed response. In the final at Munich’s Olympiastadion, Johan Neeskens converted an early penalty before Paul Breitner answered from the spot. Gerd Müller then scored just before half-time, and West Germany held on for a 2–1 victory that delivered Franz Beckenbauer and his team their second world title.', 'FRG', '2', '1', 'NED', 'Munich, West Germany', 'Final · Olympiastadion'],
  ['1978', 'Argentina', '🇦🇷', 'Argentina', '16', '38', 'A nation', 'finds its voice.', 'Argentina hosted the eleventh FIFA World Cup, a tournament that brought the national team to its first final while turning Mario Kempes into its defining star. The Netherlands pushed the hosts through a tense match at Buenos Aires’s Estadio Monumental, but Kempes opened the scoring and Dick Nanninga equalised late to force extra time. Kempes struck again before Daniel Bertoni sealed a 3–1 victory, giving Argentina its first world title in front of a home crowd.', 'ARG', '3', '1', 'NED', 'Buenos Aires, Argentina', 'Final · Monumental Stadium'],
  ['1982', 'Spain', '🇮🇹', 'Italy', '24', '52', 'Three goals', 'and a third star.', 'Spain hosted the twelfth FIFA World Cup, a demanding tournament that expanded to 24 teams and culminated in Paolo Rossi’s remarkable return to form. After Italy edged past Brazil in a legendary three-goal quarter-final, Rossi struck twice against Poland before scoring again in the final at Madrid’s Santiago Bernabéu. Italy defeated West Germany 3–1, with Marco Tardelli and Alessandro Altobelli joining Rossi on the scoresheet as Dino Zoff lifted a third world title for the Azzurri.', 'ITA', '3', '1', 'FRG', 'Madrid, Spain', 'Final · Santiago Bernabéu'],
  ['1986', 'Mexico', '🇦🇷', 'Argentina', '24', '52', 'One player', 'against the world.', 'Mexico hosted the thirteenth FIFA World Cup, where Diego Maradona became the tournament’s central figure. He scored twice against England in a quarter-final that produced both the Hand of God and the Goal of the Century, then supplied the pass for Jorge Burruchaga’s winning goal in the final. Argentina beat West Germany 3–2 at the Azteca, recovering from a late equaliser to claim its second world title.', 'ARG', '3', '2', 'FRG', 'Mexico City, Mexico', 'Final · Estadio Azteca'],
  ['1990', 'Italy', '🇩🇪', 'West Germany', '24', '52', 'A narrow', 'victory.', 'Italy hosted the fourteenth FIFA World Cup, a tournament remembered for tight defending, packed stadiums and the emergence of Salvatore Schillaci as its unexpected scoring star. West Germany navigated a demanding knockout path before meeting Argentina again in the final at Rome’s Stadio Olimpico. Andreas Brehme converted a late penalty to secure a 1–0 victory, giving Franz Beckenbauer’s team its third world title and completing a remarkable cycle after the 1986 final defeat.', 'FRG', '1', '0', 'ARG', 'Rome, Italy', 'Final · Stadio Olimpico'],
  ['1994', 'USA', '🇧🇷', 'Brazil', '24', '52', 'The first final', 'from the spot.', 'The United States hosted the fifteenth FIFA World Cup, a landmark tournament that brought football to packed stadiums across the country. Brazil combined a disciplined defence with the creativity of Romário and Bebeto, while Italy fought through a demanding knockout run led by Roberto Baggio. After a goalless final at Pasadena’s Rose Bowl, Brazil won the first World Cup decided by a penalty shootout, taking the trophy 3–2 from the spot and claiming a fourth world title.', 'BRA', '0', '0', 'ITA', 'Pasadena, USA', 'Final · Rose Bowl · Brazil won 3–2 on penalties'],
  ['1998', 'France', '🇫🇷', 'France', '32', '64', 'A home crowd', 'gets its moment.', 'France hosted the 16th FIFA World Cup across ten stadiums, bringing 32 teams together for the first time in the tournament’s history. The hosts grew into the competition behind the creativity of Zinedine Zidane, the pace of Thierry Henry and the calm leadership of Didier Deschamps, while Croatia announced itself with Davor Šuker’s goals and a surprise run to the semi-finals. In the final at the Stade de France, Zidane scored twice from corners before Emmanuel Petit added a third late on, giving France a 3–0 victory over Brazil and its first world title in front of a home crowd.', 'FRA', '3', '0', 'BRA', 'Saint-Denis, France', 'Final · Stade de France'],
  ['2002', 'Korea + Japan', '🇧🇷', 'Brazil', '32', '64', 'The fifth star', 'under new lights.', 'The first World Cup staged in Asia was shared by South Korea and Japan, and it produced a tournament of surprises: defending champions France went out in the group stage, South Korea reached the semi-finals, and Brazil’s attack found its rhythm under the bright stadium lights. Ronaldo Nazário returned from injury to lead the scoring, finishing the final in Yokohama with both goals against Germany, including the decisive finish after Oliver Kahn’s only major error of the tournament. Brazil’s 2–0 victory delivered a record fifth world title and made Ronaldo’s comeback the defining image of Korea and Japan 2002.', 'BRA', '2', '0', 'GER', 'Yokohama, Japan', 'Final · International Stadium Yokohama'],
  ['2006', 'Germany', '🇮🇹', 'Italy', '32', '64', 'A final', 'of nerve.', 'Germany hosted a tournament of packed stadiums, high energy and unforgettable drama, from Germany’s late run to the semi-finals to Italy’s disciplined rise through the knockout stage. Fabio Cannavaro anchored a defence that conceded only two goals all tournament, while Miroslav Klose won the Golden Boot and Zinedine Zidane carried France back to the final. In Berlin, Zidane opened the scoring with a Panenka penalty before Marco Materazzi equalised, and the match stayed level through extra time. Italy finally prevailed 5–3 on penalties after Zidane was sent off for his headbutt on Materazzi, lifting a fourth world title in one of the most memorable finals in World Cup history.', 'ITA', '1', '1', 'FRA', 'Berlin, Germany', 'Final · Olympiastadion · Italy won 5–3 on penalties'],
  ['2010', 'South Africa', '🇪🇸', 'Spain', '32', '64', 'A new champion', 'for a new continent.', 'South Africa hosted the first FIFA World Cup on the African continent, a tournament remembered for vuvuzelas, bright stadiums and Spain’s patient possession football. The Netherlands reached the final with a bruising, disciplined style, while Spain’s golden generation built around Xavi, Andrés Iniesta and Sergio Busquets controlled matches through movement and passing. In Johannesburg, the final stayed goalless through 90 minutes before Iniesta struck in extra time, sending a low finish beyond Maarten Stekelenburg and giving Spain its first world title in a tense 1–0 victory.', 'ESP', '1', '0', 'NED', 'Johannesburg, South Africa', 'Final · Soccer City'],
  ['2014', 'Brazil', '🇩🇪', 'Germany', '32', '64', 'A finish', 'in extra time.', 'Brazil hosted a vibrant, high-scoring World Cup that filled twelve stadiums and introduced a new generation of stars to a global audience. Germany grew stronger with each round, while the Netherlands impressed with a penalty shootout win over Costa Rica and Argentina relied on Lionel Messi’s creativity to reach the final. After Brazil’s unforgettable semi-final defeat to Germany, the final in Rio was decided by a moment of patience: Mario Götze controlled André Schürrle’s cross on his chest and volleyed past Sergio Romero in extra time, giving Germany a 1–0 victory and its fourth world title.', 'GER', '1', '0', 'ARG', 'Rio de Janeiro, Brazil', 'Final · Maracanã'],
  ['2018', 'Russia', '🇫🇷', 'France', '32', '64', 'Youthful energy', 'takes the stage.', 'Russia hosted a vivid, wide-open World Cup that introduced video assistant refereeing to the tournament and brought packed stadiums to eleven host cities. France blended the experience of Hugo Lloris and Olivier Giroud with the speed of a teenage Kylian Mbappé, while Croatia overcame extra-time matches against Denmark and England to reach its first final. In Moscow, France survived a thrilling contest with Croatia, scoring through an own goal, a penalty and strikes from Paul Pogba and Mbappé before Mario Mandžukić pulled one back. The 4–2 victory delivered France’s second world title and announced a new generation of champions.', 'FRA', '4', '2', 'CRO', 'Moscow, Russia', 'Final · Luzhniki Stadium'],
  ['2022', 'Qatar', '🇦🇷', 'Argentina', '32', '64', 'A captain', 'completes the story.', 'Qatar staged the first World Cup in the Arab world, a compact winter tournament that brought dramatic nights, new stadiums and a memorable shift in football’s global map. Argentina began with a shock defeat to Saudi Arabia but recovered behind Lionel Messi’s goals and the energy of Julián Álvarez, while Morocco became the first African team to reach a World Cup semi-final. The final in Lusail became an instant classic as Argentina and France traded six goals, with Messi and Kylian Mbappé both scoring twice before the match was decided on penalties. Argentina won 4–2 from the spot, giving Messi his first World Cup and the country its third title.', 'ARG', '3', '3', 'FRA', 'Lusail, Qatar', 'Final · Lusail Stadium · Argentina won 4–2 on penalties'],
  ['2026', 'Canada · Mexico · USA', '🇪🇸', 'Spain', '48', '104', 'A wider world', 'takes the field.', 'The expanded 2026 World Cup brought 48 teams together across Canada, Mexico and the United States, turning the tournament into a truly continental event with matches spread across sixteen host cities. Spain paired patient possession with a new generation of energy, while Argentina arrived as defending champions and pushed the final deep into extra time. At New York New Jersey Stadium, Ferran Torres scored the decisive goal in the 106th minute, giving Spain a 1–0 victory over Argentina and a second world title in a final that closed the biggest World Cup in history.', 'ESP', '1', '0', 'ARG', 'East Rutherford, USA', 'Final · New York New Jersey Stadium'],
  ['2030', 'Spain · Portugal · Morocco · Argentina · Paraguay · Uruguay', '', 'Future tournament', '48', '104', 'A new century', 'starts here.', 'The 2030 FIFA World Cup will turn its centenary into a six-country celebration across three continents. Spain, Portugal and Morocco will host the main tournament, while Argentina, Paraguay and Uruguay will stage one centenary match each in South America, returning the competition to the place where the first World Cup began in 1930. The edition will connect European, African and South American football cultures through a shared history, long-distance journeys and a format designed to make the hundred-year milestone feel global from the opening whistle.', '—', '—', '—', '—', 'Spain · Portugal · Morocco · Argentina · Paraguay · Uruguay', 'Future · 100 years after 1930']
];

const countryNames = {
  URU: 'Uruguay',
  ARG: 'Argentina',
  ITA: 'Italy',
  TCH: 'Czechoslovakia',
  HUN: 'Hungary',
  BRA: 'Brazil',
  SWE: 'Sweden',
  ENG: 'England',
  FRG: 'West Germany',
  NED: 'Netherlands',
  FRA: 'France',
  GER: 'Germany',
  ESP: 'Spain',
  CRO: 'Croatia'
};

const countryColors = {
  Uruguay: '#80BBFF',
  Italy: '#0048BA',
  France: '#17367F',
  Brazil: '#FFE540',
  England: '#fe080a',
  Argentina: '#b2def2',
  Spain: '#D71726',
  Germany: '#ffffff',
  'West Germany': '#ffffff',
  'Future tournament': '#cbd1d8'
};

const list = document.querySelector('#tournament-list');
list.innerHTML = tournamentData.map((item, index) => {
  const [year, host, flag, winner, teams, matches, title, titleAccent, story, home, homeScore, awayScore, away, location, finalLabel] = item;
  const isFuture = year === '2030';
  const bandHeader = `
    <div class="band-title"><span class="band-year">${year}</span><span class="band-country">${host}</span></div>
    <div class="band-winner"><span class="winner-label">${isFuture ? 'Next up' : 'Winner'}</span><span>${isFuture ? '<span class="trophy-icon" role="img" aria-label="World Cup trophy">🏆</span>' : `${flag} ${winner}`}</span></div>
    <div class="band-stat"><span>${teams} teams</span><span>${matches} matches</span></div>
    <div class="band-arrow" aria-hidden="true"></div>`;
  const detail = `
    <div class="tournament-detail" inert aria-hidden="true">
      <div class="detail-header"><div class="band-row">${bandHeader}</div></div>
      <div class="detail-body">
        <div class="detail-image image-${year}" role="img" aria-label="${year === '1998' ? 'France’s 1998 World Cup winners celebrate on an open-top parade bus' : year === '1962' ? 'Garrincha dribbles the ball during the 1962 World Cup' : year === '2030' ? 'The FIFA World Cup trophy on display in Toronto' : `Editorial football photograph from the ${year} World Cup in ${host}`}"></div>
        <div class="detail-copy">
          <div class="detail-topline"><span>${location || host}</span><span>${isFuture ? '2030' : year === '1934' ? '27 May – 10 June' : year === '1938' ? '4 JUNE - 19 JUNE' : year === '1950' ? '24 June – 16 July' : year === '1954' ? '16 June – 4 July' : year === '1958' ? '8 June – 29 June' : year === '1962' ? '30 May – 17 June' : year === '1966' ? '11 July – 30 July' : year === '1970' ? '31 May – 21 June' : year === '1974' ? '13 June – 7 July' : year === '1978' ? '1 June – 25 June' : year === '1982' ? '13 June – 11 July' : year === '1986' ? '31 May – 29 June' : year === '1990' ? '8 June – 8 July' : year === '1994' ? 'June 17 – July 17' : year === '1998' ? '10 June – 12 July' : year === '2002' ? '31 May – 30 June' : year === '2006' ? '9 June – 9 July' : year === '2010' ? '11 June – 11 July' : year === '2014' ? '12 June – 13 July' : year === '2018' ? '14 June – 15 July' : year === '2022' ? '20 November – 18 December' : year === '2026' ? '11 June – 19 July' : '13 July — 30 July'}</span></div>
          <h2>${title}<br /><em>${titleAccent}</em></h2>
          <p>${story || 'A tournament remembered through its host country, its champions and the moments that still echo through the game.'}</p>
          <a class="tournament-link" href="tournament-${year}.html">Explore ${year} tournament <span aria-hidden="true">↗</span></a>
          <div class="detail-footer"><span class="score">${homeScore && homeScore !== '—' ? `${countryNames[home] || home} <b>${homeScore}</b> — <b>${awayScore}</b> ${countryNames[away] || away}` : (isFuture ? 'Details to come' : `${winner} · Winner`)}</span><span>${finalLabel || ''}</span></div>
        </div>
      </div>
    </div>`;
  return `<article class="tournament" id="tournament-${year}" role="listitem" tabindex="0" data-index="${index}" data-year="${year}" aria-label="${year} ${host} World Cup, ${isFuture ? 'upcoming' : `winner ${winner}`}" aria-current="false">
    <div class="band-row">${bandHeader}</div>
    ${detail}
  </article>`;
}).join('');

const tournaments = [...document.querySelectorAll('.tournament')];
let activeIndex = null;

function setActiveTournament(index) {
  const nextIndex = index;
  activeIndex = nextIndex;
  tournaments.forEach((tournament, i) => {
    const active = i === nextIndex;
    tournament.classList.toggle('is-active', active);
    tournament.setAttribute('aria-current', active ? 'true' : 'false');
    const detail = tournament.querySelector('.tournament-detail');
    detail.inert = !active;
    detail.setAttribute('aria-hidden', String(!active));
  });
}

function toggleTournament(index) {
  const nextIndex = activeIndex === index ? null : index;
  setActiveTournament(nextIndex);
}

tournaments.forEach((tournament, index) => {
  tournament.addEventListener('focus', () => {
    if (tournament.matches(':focus-visible')) setActiveTournament(index);
  });
  tournament.addEventListener('click', (event) => {
    if (tournament.classList.contains('is-active') && !event.target.closest('.detail-header')) return;
    toggleTournament(index);
  });
  tournament.addEventListener('keydown', (event) => {
    if (event.target.closest('a, button, input, select, textarea')) return;
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      toggleTournament(index);
      return;
    }
    if (event.key === 'ArrowDown' || event.key === 'ArrowRight') {
      if (index === tournaments.length - 1) return;
      event.preventDefault();
      const next = tournaments[index + 1];
      setActiveTournament(index + 1);
      next.focus();
    }
    if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') {
      if (index === 0) return;
      event.preventDefault();
      const previous = tournaments[index - 1];
      setActiveTournament(index - 1);
      previous.focus();
    }
  });
});

const linkedTournament = tournaments.find((tournament) => `#${tournament.id}` === window.location.hash);
if (linkedTournament) {
  setActiveTournament(Number(linkedTournament.dataset.index));
  requestAnimationFrame(() => linkedTournament.scrollIntoView({ block: 'start' }));
}
