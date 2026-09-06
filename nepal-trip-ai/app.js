const searchForm = document.querySelector('#trip-search');
const destinationInput = document.querySelector('#destination-input');
const moodSelect = document.querySelector('#mood-select');
const resultMessage = document.querySelector('#search-result');
const emptyState = document.querySelector('#empty-state');
const cards = [...document.querySelectorAll('.destination-card')];
const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('#main-nav');

function filterTrips(event) {
  event.preventDefault();
  const query = destinationInput.value.trim().toLowerCase();
  const mood = moodSelect.value;
  let visibleCount = 0;

  cards.forEach((card) => {
    const matchesQuery = !query || card.dataset.name.includes(query);
    const matchesMood = mood === 'all' || card.dataset.mood === mood;
    const isVisible = matchesQuery && matchesMood;
    card.hidden = !isVisible;
    if (isVisible) visibleCount += 1;
  });

  emptyState.hidden = visibleCount > 0;
  resultMessage.textContent = visibleCount > 0 ? `${visibleCount} journey${visibleCount === 1 ? '' : 's'} found for you.` : '';
}

searchForm.addEventListener('submit', filterTrips);

moodSelect.addEventListener('change', () => {
  filterTrips({ preventDefault: () => {} });
});

document.querySelectorAll('.save-button').forEach((button) => {
  button.addEventListener('click', () => {
    const isSaved = button.classList.toggle('saved');
    button.textContent = isSaved ? '♥' : '♡';
    button.setAttribute('aria-label', isSaved ? 'Remove from saved trips' : 'Save this trip');
  });
});

menuToggle.addEventListener('click', () => {
  const isOpen = mainNav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
  menuToggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
});

document.querySelectorAll('.main-nav a').forEach((link) => {
  link.addEventListener('click', () => {
    mainNav.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
  });
});
