const teamButtons = [...document.querySelectorAll('.team-row[data-team]')];
let profilesPromise;
let lineupPanelId = 0;

const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
})[character]);

const number = (value) => Number(value ?? 0).toLocaleString('en');
const resultCount = (value, singular, plural) => `${number(value)} ${Number(value) === 1 ? singular : plural}`;
const placementLabel = (placement) => {
  if (placement === 'Champion') return 'Champions';
  if (placement === 'Runner-up') return 'Runners-up';
  return placement;
};

function getProfiles() {
  if (!profilesPromise) {
    profilesPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'data/team-directory-details.js';
      script.onload = () => {
        script.remove();
        if (window.worldCupTeamProfiles) resolve(window.worldCupTeamProfiles);
        else reject(new Error('Team details script did not provide profiles'));
      };
      script.onerror = () => {
        script.remove();
        reject(new Error('Could not load team details'));
      };
      document.head.append(script);
    });
  }
  return profilesPromise;
}

function renderMatchSide(name, venue, players, substitutions, scorers) {
  const starters = players.map((player) => `<li>${escapeHtml(player)}</li>`).join('');
  const goals = scorers.length
    ? `<ul class="team-lineup-scorers">${scorers.map((scorer) => `<li><span class="team-lineup-minute">${escapeHtml(scorer.minute)}′</span><span><strong>${escapeHtml(scorer.player)}</strong>${scorer.penalty ? ' (pen.)' : ''}${scorer.own_goal ? ' (own goal)' : ''}</span></li>`).join('')}</ul>`
    : '<p class="team-lineup-none">No scorers</p>';
  const changes = substitutions.length
    ? `<ul class="team-lineup-substitutions">${substitutions.map((substitution) => `<li><span class="team-lineup-minute">${escapeHtml(substitution.minute)}′</span><span><strong>${escapeHtml(substitution.player_on)}</strong> on <span class="team-lineup-off">· ${escapeHtml(substitution.player_off)} off</span></span></li>`).join('')}</ul>`
    : '<p class="team-lineup-none">No substitutions</p>';
  return `<section class="team-lineup-side">
    <h4><span>${escapeHtml(venue)}</span>${escapeHtml(name)}</h4>
    <h5>Scorers</h5>
    ${goals}
    <h5>Starting lineup</h5>
    <ul class="team-lineup-starters">${starters}</ul>
    <h5>Substitutions</h5>
    ${changes}
  </section>`;
}

function renderMatch(match, teamName) {
  const date = new Date(`${match.date}T12:00:00Z`).toLocaleDateString('en-GB', {
    day: 'numeric', month: 'short', timeZone: 'UTC',
  });
  const result = match.result;
  const shootout = match.penalty_shootout;
  const penaltyOutcome = shootout?.result === 'win' ? 'Won' : 'Lost';
  const penaltyNote = shootout
    ? `<span class="team-match-penalties team-match-penalties--full">${penaltyOutcome} ${escapeHtml(shootout.score.for)}–${escapeHtml(shootout.score.against)} on penalties</span><span class="team-match-penalties team-match-penalties--short">${penaltyOutcome} (${escapeHtml(shootout.score.for)}-${escapeHtml(shootout.score.against)} p.)</span>`
    : '';
  const homeName = match.home_away === 'home' ? teamName : match.opponent;
  const awayName = match.home_away === 'away' ? teamName : match.opponent;
  const teamSide = match.home_away;
  const opponentSide = teamSide === 'home' ? 'away' : 'home';
  const available = { home: new Set(match.lineup.home), away: new Set(match.lineup.away) };
  const substitutions = { home: [], away: [] };
  for (const substitution of match.substitutions) {
    const side = available.home.has(substitution.player_off) ? 'home'
      : available.away.has(substitution.player_off) ? 'away'
      : substitution.team === homeName ? 'home' : 'away';
    substitutions[side].push(substitution);
    available[side].add(substitution.player_on);
  }
  const scorers = { home: [], away: [] };
  for (const scorer of match.scorers) {
    const playerSide = available.home.has(scorer.player) ? 'home' : 'away';
    const creditedSide = scorer.own_goal ? (playerSide === 'home' ? 'away' : 'home') : playerSide;
    scorers[creditedSide].push(scorer);
  }
  const panelId = `team-lineup-${++lineupPanelId}`;
  return `<li class="team-match">
    <time datetime="${escapeHtml(match.date)}">${escapeHtml(date)}</time>
    <span class="team-match-opponent">${escapeHtml(match.opponent)}</span>
    <strong class="team-match-score" aria-label="${escapeHtml(teamName)} ${escapeHtml(match.score.for)}, ${escapeHtml(match.opponent)} ${escapeHtml(match.score.against)}">${escapeHtml(match.score.for)}–${escapeHtml(match.score.against)}</strong>
    <span class="team-match-outcome team-match-outcome--${escapeHtml(result)}">${escapeHtml(result)}</span>
    <span class="team-match-context"><span class="team-match-stage">${escapeHtml(match.stage)}</span>${penaltyNote}</span>
    <button class="team-lineup-toggle" type="button" aria-expanded="false" aria-controls="${panelId}" aria-label="Details for ${escapeHtml(teamName)} vs ${escapeHtml(match.opponent)}, ${escapeHtml(date)}"><span class="team-lineup-chevron" aria-hidden="true">▸</span><span>Details</span></button>
    <div class="team-match-lineup-panel" id="${panelId}" hidden>
      ${renderMatchSide(teamName, teamSide, match.lineup[teamSide], substitutions[teamSide], scorers[teamSide])}
      ${renderMatchSide(match.opponent, opponentSide, match.lineup[opponentSide], substitutions[opponentSide], scorers[opponentSide])}
    </div>
  </li>`;
}

function renderTournament(tournament, teamName) {
  const year = escapeHtml(tournament.year);
  const matchCount = tournament.matches.length;
  return `<li class="team-tournament">
    <div class="team-tournament-main">
      <div class="team-tournament-edition"><strong>${year}</strong><span>${escapeHtml(tournament.host)}</span></div>
      <div class="team-tournament-result"><strong>${escapeHtml(placementLabel(tournament.best_placement))}</strong><span>${number(tournament.matches_played)} matches played</span><span>${resultCount(tournament.wins, 'Win', 'Wins')} · ${resultCount(tournament.draws, 'Draw', 'Draws')} · ${resultCount(tournament.losses, 'Loss', 'Losses')}</span></div>
      <div class="team-tournament-goals"><span>Goals</span><strong>${number(tournament.goals_for)}–${number(tournament.goals_against)}</strong></div>
      <a class="team-tournament-link" href="tournament-${year}.html" aria-label="Explore the ${year} World Cup">Explore <span aria-hidden="true">↗</span></a>
    </div>
    <details class="team-match-disclosure"><summary>Match results <span>${matchCount}</span></summary>
      <ol class="team-match-list">${tournament.matches.map((match) => renderMatch(match, teamName)).join('')}</ol>
    </details>
  </li>`;
}

function renderCrest(crest) {
  if (crest.kind === 'image') {
    return `<img class="team-crest team-detail-crest" src="${escapeHtml(crest.src)}" alt="">`;
  }
  if (crest.kind === 'flag') {
    return `<span class="team-crest team-crest-flag team-detail-crest" aria-hidden="true"><img src="${escapeHtml(crest.src)}" alt=""></span>`;
  }
  return `<span class="team-crest team-crest-fallback team-detail-crest" aria-hidden="true">${escapeHtml(crest.text)}</span>`;
}

function renderProfile(profile) {
  const best = profile.best_placement;
  const totals = profile.totals;
  const isChampion = best.placement === 'Champion';
  const bestYears = best.years.map((year) => isChampion
    ? `<span class="team-best-year">${escapeHtml(year)}<span class="team-title-trophy" aria-hidden="true">🏆</span></span>`
    : escapeHtml(year)).join(' · ');
  return `<div class="team-detail-inner">
    <div class="team-detail-overview">
      <div class="team-profile-heading">
        ${renderCrest(profile.crest)}
        <div class="team-best-finish">
          <h2>Best finish</h2>
          <p>${escapeHtml(placementLabel(best.placement))}</p>
          <span>${bestYears}</span>
        </div>
      </div>
      <dl class="team-total-stats">
        <div><dt>World Cups</dt><dd>${number(profile.tournaments.length)}</dd></div>
        <div><dt>Matches</dt><dd>${number(totals.matches_played)}</dd></div>
        <div><dt>Wins</dt><dd>${number(totals.wins)}</dd></div>
        <div><dt>Draws</dt><dd>${number(totals.draws)}</dd></div>
        <div><dt>Losses</dt><dd>${number(totals.losses)}</dd></div>
        <div><dt>Goals for</dt><dd>${number(totals.goals_for)}</dd></div>
        <div><dt>Goals against</dt><dd>${number(totals.goals_against)}</dd></div>
      </dl>
    </div>
    <details class="team-tournament-history" aria-label="${escapeHtml(profile.name)} tournament history">
      <summary class="team-history-heading"><span class="team-history-title" role="heading" aria-level="3">Tournament history</span><span class="team-history-meta"><span class="team-history-prompt">Click to expand</span><span class="team-history-chevron" aria-hidden="true">⌄</span></span></summary>
      <ol class="team-tournament-list">${profile.tournaments.map((tournament) => renderTournament(tournament, profile.name)).join('')}</ol>
    </details>
  </div>`;
}

function closeTeam(button) {
  if (!button || button.getAttribute('aria-expanded') !== 'true') return;
  button.setAttribute('aria-expanded', 'false');
  button.closest('.team-item').classList.remove('is-open');
  document.getElementById(button.getAttribute('aria-controls')).hidden = true;
}

async function toggleTeam(button) {
  if (button.getAttribute('aria-expanded') === 'true') {
    closeTeam(button);
    return;
  }
  const openButton = document.querySelector('.team-row[aria-expanded="true"]');
  closeTeam(openButton);
  const adjustScroll = () => {
    if (openButton && button.getAttribute('aria-expanded') === 'true') {
      button.scrollIntoView({ block: 'start' });
    }
  };

  const panel = document.getElementById(button.getAttribute('aria-controls'));
  button.setAttribute('aria-expanded', 'true');
  button.closest('.team-item').classList.add('is-open');
  panel.hidden = false;
  if (panel.dataset.loaded) {
    adjustScroll();
    return;
  }

  panel.innerHTML = '<p class="team-detail-loading" role="status">Loading team history…</p>';
  try {
    const profiles = await getProfiles();
    panel.innerHTML = renderProfile(profiles[button.dataset.team]);
    panel.dataset.loaded = 'true';
  } catch (error) {
    panel.innerHTML = '<p class="team-detail-loading" role="alert">Team history could not be loaded. Please try again.</p>';
    profilesPromise = undefined;
  } finally {
    adjustScroll();
  }
}

teamButtons.forEach((button, index) => {
  button.addEventListener('click', () => toggleTeam(button));
  button.addEventListener('keydown', (event) => {
    const targets = {
      ArrowDown: Math.min(index + 1, teamButtons.length - 1),
      ArrowUp: Math.max(index - 1, 0),
      Home: 0,
      End: teamButtons.length - 1,
    };
    if (event.key in targets) {
      event.preventDefault();
      teamButtons[targets[event.key]].focus();
    } else if (event.key === 'Escape') {
      closeTeam(button);
    }
  });
});

document.querySelector('.team-list').addEventListener('click', (event) => {
  const button = event.target.closest('.team-lineup-toggle');
  if (!button) return;
  const expanded = button.getAttribute('aria-expanded') === 'true';
  button.setAttribute('aria-expanded', String(!expanded));
  document.getElementById(button.getAttribute('aria-controls')).hidden = expanded;
});
