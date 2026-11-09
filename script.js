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
    if (active) {
      detail.querySelectorAll('img[data-src]').forEach((image) => {
        image.src = image.dataset.src;
        delete image.dataset.src;
      });
    }
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
  setActiveTournament(tournaments.indexOf(linkedTournament));
  requestAnimationFrame(() => linkedTournament.scrollIntoView({ block: 'start' }));
}
