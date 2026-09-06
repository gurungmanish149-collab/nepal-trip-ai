const searchForm = document.querySelector('#trip-search');
const destinationInput = document.querySelector('#destination-input');
const moodSelect = document.querySelector('#mood-select');
const resultMessage = document.querySelector('#search-result');
const emptyState = document.querySelector('#empty-state');
const cards = [...document.querySelectorAll('.destination-card')];
const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('#main-nav');
const languageButton = document.querySelector('#language-button');
const languageMenu = document.querySelector('#language-menu');
const currentLanguageLabel = document.querySelector('#current-language');

const translations = {
  en: {
    label: 'EN',
    mainNavLabel: 'Main navigation',
    explore: 'Discover',
    howItWorks: 'My trips',
    stories: 'Profile',
    signIn: 'Sign in',
    openMenu: 'Open menu',
    closeMenu: 'Close menu',
    heroEyebrow: 'Your trip dashboard',
    heroTitle: 'Where will you<br /><em>go next?</em>',
    heroCopy: 'Build a trip around your time, energy, and the kind of stories you want to bring home.',
    startExploring: 'Plan a new trip',
    watchStory: 'View saved trips',
    seeStory: 'View saved trips',
    heroNote: 'Kathmandu<br /><strong>18°C · Clear</strong>',
    scrollToExplore: '3 saved trips',
    curatedForYou: 'AI recommendations',
    exploreTitle: 'Explore Nepal<br /><em>your way.</em>',
    sectionIntro: 'Routes matched to your time, energy, and the kind of stories you want to bring home.',
    dreamingOf: "I'm dreaming of",
    destinationPlaceholder: 'A place or experience',
    travelMood: 'My travel mood',
    moodAll: 'Any kind of adventure',
    moodMountains: 'Mountain air',
    moodCulture: 'Culture & calm',
    moodWild: 'Wild escapes',
    findMyTrip: 'Find my trip',
    iconicTrek: 'Iconic trek',
    slowTravel: 'Slow travel',
    intoTheWild: 'Into the wild',
    everestDays: '⌁ 14 days',
    pokharaDays: '⌁ 5 days',
    chitwanDays: '⌁ 4 days',
    challenging: '↗ Challenging',
    easy: '↗ Easy',
    gentle: '↗ Gentle',
    saveEverest: 'Save Everest Base Camp',
    savePokhara: 'Save Pokhara',
    saveChitwan: 'Save Chitwan',
    saveTrip: 'Save this trip',
    removeSaved: 'Remove from saved trips',
    emptyState: 'No journeys found yet. Try “mountain”, “Pokhara”, or choose another mood.',
    stepOne: 'Pick a place<br />or feeling',
    stepTwo: 'Shape your<br />perfect route',
    stepThree: 'Keep it<br />all together',
    trustMessage: 'Your trip, in one place<br /><span>ready when you are.</span>',
    footerTagline: 'Travel deeper. Feel more.',
    journeyFound: (count) => `${count} journey${count === 1 ? '' : 's'} found for you.`
  },
  ja: {
    label: 'JA',
    mainNavLabel: 'メインナビゲーション',
    explore: '探す',
    howItWorks: 'マイトリップ',
    stories: 'プロフィール',
    signIn: 'サインイン',
    openMenu: 'メニューを開く',
    closeMenu: 'メニューを閉じる',
    heroEyebrow: 'あなたの旅ダッシュボード',
    heroTitle: '次はどこへ<br /><em>行きますか？</em>',
    heroCopy: '時間と体力、旅から持ち帰りたい物語に合わせて旅をつくりましょう。',
    startExploring: '新しい旅を計画',
    watchStory: '保存した旅を見る',
    seeStory: '保存した旅を見る',
    heroNote: 'カトマンズ<br /><strong>18°C · 晴れ</strong>',
    scrollToExplore: '保存した旅 3件',
    curatedForYou: 'AIおすすめ',
    exploreTitle: 'ネパールを探す<br /><em>あなたらしく。</em>',
    sectionIntro: '時間、体力、持ち帰りたい物語に合わせたルートをご提案します。',
    dreamingOf: '夢見ている場所',
    destinationPlaceholder: '場所や体験を入力',
    travelMood: '旅の気分',
    moodAll: 'すべての冒険',
    moodMountains: '山の空気',
    moodCulture: '文化と癒やし',
    moodWild: '野生の旅',
    findMyTrip: '旅を見つける',
    iconicTrek: '憧れのトレッキング',
    slowTravel: 'ゆっくり旅',
    intoTheWild: '大自然へ',
    everestDays: '⌁ 14日間',
    pokharaDays: '⌁ 5日間',
    chitwanDays: '⌁ 4日間',
    challenging: '↗ 上級',
    easy: '↗ 初級',
    gentle: '↗ やさしい',
    saveEverest: 'エベレスト・ベースキャンプを保存',
    savePokhara: 'ポカラを保存',
    saveChitwan: 'チトワンを保存',
    saveTrip: 'この旅を保存',
    removeSaved: '保存済みの旅から削除',
    emptyState: '旅が見つかりません。「山」「ポカラ」または別の気分を試してください。',
    stepOne: '場所や気分を<br />選ぶ',
    stepTwo: 'ぴったりのルートを<br />つくる',
    stepThree: '旅をひとつに<br />まとめる',
    trustMessage: '旅をひとつの場所に<br /><span>いつでも準備万端。</span>',
    footerTagline: '深く旅して、もっと感じる。',
    journeyFound: (count) => `${count}件の旅が見つかりました。`
  },
  zh: {
    label: 'ZH',
    mainNavLabel: '主导航',
    explore: '探索',
    howItWorks: '我的旅程',
    stories: '个人资料',
    signIn: '登录',
    openMenu: '打开菜单',
    closeMenu: '关闭菜单',
    heroEyebrow: '你的旅行仪表盘',
    heroTitle: '下一站要去<br /><em>哪里？</em>',
    heroCopy: '根据时间、体力和想带回家的故事，规划一段属于你的旅程。',
    startExploring: '规划新旅程',
    watchStory: '查看已保存旅程',
    seeStory: '查看已保存旅程',
    heroNote: '加德满都<br /><strong>18°C · 晴</strong>',
    scrollToExplore: '已保存 3 段旅程',
    curatedForYou: 'AI 为你推荐',
    exploreTitle: '探索尼泊尔<br /><em>找到你的方式。</em>',
    sectionIntro: '根据你的时间、体力和想带回家的故事，为你匹配路线。',
    dreamingOf: '我向往的地方',
    destinationPlaceholder: '地点或体验',
    travelMood: '我的旅行心情',
    moodAll: '任何冒险',
    moodMountains: '山间清风',
    moodCulture: '文化与宁静',
    moodWild: '野外探索',
    findMyTrip: '寻找我的旅程',
    iconicTrek: '经典徒步',
    slowTravel: '慢旅行',
    intoTheWild: '走进荒野',
    everestDays: '⌁ 14天',
    pokharaDays: '⌁ 5天',
    chitwanDays: '⌁ 4天',
    challenging: '↗ 高难度',
    easy: '↗ 轻松',
    gentle: '↗ 温和',
    saveEverest: '保存珠峰大本营',
    savePokhara: '保存博卡拉',
    saveChitwan: '保存奇特旺',
    saveTrip: '保存这段旅程',
    removeSaved: '从已保存旅程中移除',
    emptyState: '暂时没有找到旅程。试试“山脉”“博卡拉”，或选择另一种心情。',
    stepOne: '选择地点<br />或心情',
    stepTwo: '规划你的<br />完美路线',
    stepThree: '把旅程<br />放在一起',
    trustMessage: '让旅程集中在<br /><span>一个随时可用的地方。</span>',
    footerTagline: '深入旅行，感受更多。',
    journeyFound: (count) => `为你找到${count}段旅程。`
  },
  ko: {
    label: 'KO',
    mainNavLabel: '메인 탐색',
    explore: '둘러보기',
    howItWorks: '내 여행',
    stories: '프로필',
    signIn: '로그인',
    openMenu: '메뉴 열기',
    closeMenu: '메뉴 닫기',
    heroEyebrow: '나의 여행 대시보드',
    heroTitle: '다음에는<br /><em>어디로 갈까요?</em>',
    heroCopy: '시간과 체력, 집으로 가져오고 싶은 이야기에 맞춰 여행을 만들어보세요.',
    startExploring: '새 여행 계획하기',
    watchStory: '저장한 여행 보기',
    seeStory: '저장한 여행 보기',
    heroNote: '카트만두<br /><strong>18°C · 맑음</strong>',
    scrollToExplore: '저장한 여행 3개',
    curatedForYou: 'AI 추천',
    exploreTitle: '네팔 탐색하기<br /><em>나만의 방식으로.</em>',
    sectionIntro: '시간과 체력, 집으로 가져오고 싶은 이야기에 맞는 루트를 추천해드려요.',
    dreamingOf: '꿈꾸는 여행지',
    destinationPlaceholder: '장소 또는 경험',
    travelMood: '나의 여행 기분',
    moodAll: '어떤 모험이든',
    moodMountains: '산의 공기',
    moodCulture: '문화와 휴식',
    moodWild: '야생 속으로',
    findMyTrip: '내 여행 찾기',
    iconicTrek: '대표 트레킹',
    slowTravel: '느린 여행',
    intoTheWild: '야생 속으로',
    everestDays: '⌁ 14일',
    pokharaDays: '⌁ 5일',
    chitwanDays: '⌁ 4일',
    challenging: '↗ 도전적',
    easy: '↗ 쉬움',
    gentle: '↗ 여유로움',
    saveEverest: '에베레스트 베이스캠프 저장',
    savePokhara: '포카라 저장',
    saveChitwan: '치트완 저장',
    saveTrip: '이 여행 저장',
    removeSaved: '저장한 여행에서 삭제',
    emptyState: '아직 여행을 찾지 못했어요. “산”, “포카라” 또는 다른 기분을 선택해 보세요.',
    stepOne: '장소나 기분을<br />선택하세요',
    stepTwo: '나만의 완벽한<br />루트를 만드세요',
    stepThree: '여행을 한곳에<br />모아보세요',
    trustMessage: '여행을 한곳에 모아<br /><span>언제든 준비하세요.</span>',
    footerTagline: '더 깊이 여행하고, 더 많이 느껴보세요.',
    journeyFound: (count) => `${count}개의 여행을 찾았어요.`
  }
};

let currentLanguage = localStorage.getItem('himalaya-language') || 'en';

function applyLanguage(language) {
  currentLanguage = translations[language] ? language : 'en';
  const languageCopy = translations[currentLanguage];
  document.documentElement.lang = currentLanguage;
  currentLanguageLabel.textContent = languageCopy.label;

  document.querySelectorAll('[data-i18n]').forEach((element) => {
    element.textContent = languageCopy[element.dataset.i18n];
  });
  document.querySelectorAll('[data-i18n-html]').forEach((element) => {
    element.innerHTML = languageCopy[element.dataset.i18nHtml];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
    element.placeholder = languageCopy[element.dataset.i18nPlaceholder];
  });
  document.querySelectorAll('[data-i18n-aria]').forEach((element) => {
    element.setAttribute('aria-label', languageCopy[element.dataset.i18nAria]);
  });

  document.querySelectorAll('[data-language]').forEach((option) => {
    option.classList.toggle('active', option.dataset.language === currentLanguage);
  });
  document.title = `Himalaya | ${currentLanguage === 'en' ? 'Find your Nepal' : languageCopy.explore}`;
  localStorage.setItem('himalaya-language', currentLanguage);
  updateSaveLabels();
  if (resultMessage.textContent) {
    const visibleCount = cards.filter((card) => !card.hidden).length;
    resultMessage.textContent = visibleCount ? languageCopy.journeyFound(visibleCount) : '';
  }
}

function updateSaveLabels() {
  const languageCopy = translations[currentLanguage];
  document.querySelectorAll('.save-button').forEach((button) => {
    const isSaved = button.classList.contains('saved');
    button.setAttribute('aria-label', isSaved ? languageCopy.removeSaved : languageCopy[button.dataset.i18nAria]);
  });
}

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
  resultMessage.textContent = visibleCount > 0 ? translations[currentLanguage].journeyFound(visibleCount) : '';
}

searchForm.addEventListener('submit', filterTrips);

moodSelect.addEventListener('change', () => {
  filterTrips({ preventDefault: () => {} });
});

document.querySelectorAll('.save-button').forEach((button) => {
  button.addEventListener('click', () => {
    const isSaved = button.classList.toggle('saved');
    button.textContent = isSaved ? '♥' : '♡';
    const languageCopy = translations[currentLanguage];
    button.setAttribute('aria-label', isSaved ? languageCopy.removeSaved : languageCopy[button.dataset.i18nAria]);
  });
});

menuToggle.addEventListener('click', () => {
  const isOpen = mainNav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
  menuToggle.setAttribute('aria-label', isOpen ? translations[currentLanguage].closeMenu : translations[currentLanguage].openMenu);
});

document.querySelectorAll('.main-nav a').forEach((link) => {
  link.addEventListener('click', () => {
    mainNav.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
  });
});

languageButton.addEventListener('click', () => {
  const isOpen = languageMenu.classList.toggle('open');
  languageButton.setAttribute('aria-expanded', String(isOpen));
});

document.querySelectorAll('[data-language]').forEach((option) => {
  option.addEventListener('click', () => {
    applyLanguage(option.dataset.language);
    languageMenu.classList.remove('open');
    languageButton.setAttribute('aria-expanded', 'false');
  });
});

document.addEventListener('click', (event) => {
  if (!event.target.closest('.language-picker')) {
    languageMenu.classList.remove('open');
    languageButton.setAttribute('aria-expanded', 'false');
  }
});

applyLanguage(currentLanguage);
