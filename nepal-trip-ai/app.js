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
    explore: 'Explore',
    howItWorks: 'How it works',
    stories: 'Stories',
    signIn: 'Sign in',
    openMenu: 'Open menu',
    closeMenu: 'Close menu',
    heroEyebrow: 'Your intelligent Nepal guide',
    heroTitle: 'Find the Nepal<br /><em>that calls you.</em>',
    heroCopy: 'From quiet mountain villages to wild jungle trails, discover a journey shaped around the way you want to travel.',
    startExploring: 'Start exploring',
    watchStory: 'Watch the Nepal story',
    seeStory: 'See the story',
    heroNote: 'Built for curious<br />travellers',
    scrollToExplore: 'Scroll to explore',
    curatedForYou: 'Curated for you',
    exploreTitle: 'Where will you<br /><em>go next?</em>',
    sectionIntro: 'Tell us what moves you. We’ll help you find a Nepal that feels like it was made just for you.',
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
    stepOne: 'Tell us what<br />you love',
    stepTwo: 'Meet your<br />perfect route',
    stepThree: 'Make it<br />unforgettable',
    trustMessage: 'Made with local knowledge<br /><span>and a little bit of magic.</span>',
    footerTagline: 'Travel deeper. Feel more.',
    journeyFound: (count) => `${count} journey${count === 1 ? '' : 's'} found for you.`
  },
  ja: {
    label: 'JA',
    mainNavLabel: 'メインナビゲーション',
    explore: '探す',
    howItWorks: '使い方',
    stories: 'ストーリー',
    signIn: 'サインイン',
    openMenu: 'メニューを開く',
    closeMenu: 'メニューを閉じる',
    heroEyebrow: 'あなたのネパール旅ガイド',
    heroTitle: 'あなたを呼ぶ<br /><em>ネパールへ。</em>',
    heroCopy: '静かな山村から野生のジャングルまで、あなたらしい旅を見つけよう。',
    startExploring: '旅を探す',
    watchStory: 'ネパールの物語を見る',
    seeStory: '物語を見る',
    heroNote: '好奇心を持つ<br />旅人のために',
    scrollToExplore: 'スクロールして探す',
    curatedForYou: 'あなたのために厳選',
    exploreTitle: '次はどこへ<br /><em>行きますか？</em>',
    sectionIntro: '心が動くものを教えてください。あなたのためだけのネパールを見つけます。',
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
    stepOne: '好きなものを<br />教えてください',
    stepTwo: 'ぴったりのルートに<br />出会う',
    stepThree: '忘れられない旅を<br />つくる',
    trustMessage: '現地の知識と<br /><span>少しの魔法を添えて。</span>',
    footerTagline: '深く旅して、もっと感じる。',
    journeyFound: (count) => `${count}件の旅が見つかりました。`
  },
  zh: {
    label: 'ZH',
    mainNavLabel: '主导航',
    explore: '探索',
    howItWorks: '使用方式',
    stories: '故事',
    signIn: '登录',
    openMenu: '打开菜单',
    closeMenu: '关闭菜单',
    heroEyebrow: '你的尼泊尔智能旅行向导',
    heroTitle: '寻找属于你的<br /><em>尼泊尔。</em>',
    heroCopy: '从宁静的山村到原始的丛林小径，发现一段为你量身定制的旅程。',
    startExploring: '开始探索',
    watchStory: '观看尼泊尔故事',
    seeStory: '查看故事',
    heroNote: '为充满好奇的<br />旅行者打造',
    scrollToExplore: '向下探索',
    curatedForYou: '为你精选',
    exploreTitle: '下一站要去<br /><em>哪里？</em>',
    sectionIntro: '告诉我们什么会打动你。我们将帮你找到仿佛为你而生的尼泊尔旅程。',
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
    stepOne: '告诉我们你<br />喜欢什么',
    stepTwo: '遇见你的<br />完美路线',
    stepThree: '创造一段<br />难忘旅程',
    trustMessage: '融入当地知识<br /><span>再加一点点魔法。</span>',
    footerTagline: '深入旅行，感受更多。',
    journeyFound: (count) => `为你找到${count}段旅程。`
  },
  ko: {
    label: 'KO',
    mainNavLabel: '메인 탐색',
    explore: '둘러보기',
    howItWorks: '이용 방법',
    stories: '이야기',
    signIn: '로그인',
    openMenu: '메뉴 열기',
    closeMenu: '메뉴 닫기',
    heroEyebrow: '당신을 위한 네팔 여행 가이드',
    heroTitle: '당신을 부르는<br /><em>네팔을 만나보세요.</em>',
    heroCopy: '고요한 산골 마을부터 야생의 정글 트레일까지, 당신의 방식에 맞는 여행을 발견하세요.',
    startExploring: '여행 찾아보기',
    watchStory: '네팔 이야기 보기',
    seeStory: '이야기 보기',
    heroNote: '호기심 많은<br />여행자를 위해',
    scrollToExplore: '스크롤하여 탐색',
    curatedForYou: '당신을 위해 엄선한 여행',
    exploreTitle: '다음에는<br /><em>어디로 갈까요?</em>',
    sectionIntro: '당신을 움직이는 것을 알려주세요. 당신만을 위해 만들어진 네팔을 찾아드릴게요.',
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
    stepOne: '좋아하는 것을<br />알려주세요',
    stepTwo: '완벽한 루트를<br />만나보세요',
    stepThree: '잊지 못할 여행을<br />만들어보세요',
    trustMessage: '현지 지식에<br /><span>조금의 마법을 더해.</span>',
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
