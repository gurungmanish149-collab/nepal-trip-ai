import re

from flask import Blueprint, current_app, jsonify, redirect, render_template_string, request, session, send_from_directory

from .data import DESTINATIONS
from .models import authenticate_user, create_user, find_user_by_email, find_user_by_username


pages = Blueprint("pages", __name__)
auth_api = Blueprint("auth_api", __name__)
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_PATTERN = re.compile(r"^[a-z0-9._-]{3,30}$")
ALLOWED_INTERESTS = {"mountains", "culture", "wildlife", "slow"}


def serve_page(filename):
    return send_from_directory(current_app.config["PROJECT_ROOT"], filename)


@pages.get("/")
def home():
    return serve_page("index.html")


@pages.get("/signin.html")
def signin_page():
    return serve_page("signin.html")


@pages.get("/signup.html")
def signup_page():
    return serve_page("signup.html")


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Himalaya dashboard for discovering Nepal destinations." />
  <title>Himalaya | My Nepal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans+SC:wght@400;500;700&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <style>
    body { background: #eef1ed; }
    .site-header { position: relative; min-height: 76px; padding: 0 5.5vw; color: var(--ink); background: #fbfcf9; border-bottom: 1px solid #dce2dc; }
    .brand-mark { border-color: var(--ink); color: var(--ink); }
    .main-nav { margin-left: 8%; color: #73807c; }
    .main-nav a:hover, .main-nav a.active { color: var(--ink); border-color: var(--saffron); }
    .language-button, .sign-in { color: var(--ink); }
    .sign-in { border-color: #c8d0ca; }
    .sign-in:hover { background: #edf1eb; }
    .hero.app-dashboard { min-height: 0; height: auto; max-height: none; padding: 40px 12vw 38px; color: var(--ink); background: #e2eae3; overflow: visible; }
    .hero.app-dashboard::after { display: none; }
    .app-dashboard .hero-content { max-width: 680px; }
    .app-dashboard .hero-copy { max-width: 510px; color: #657572; }
    .app-dashboard h1 { font-size: clamp(2.8rem, 4.8vw, 4.4rem); letter-spacing: -3px; }
    .app-dashboard .hero-note { top: 50%; right: 12vw; padding: 16px 20px 16px 15px; color: var(--ink); background: rgba(255,255,255,.65); border: 1px solid rgba(16,45,50,.12); box-shadow: 0 12px 25px rgba(16,45,50,.06); }
    .app-dashboard .hero-note-icon { background: var(--saffron); color: var(--ink); border: 0; }
    .app-dashboard .hero-note strong { font-size: 12px; font-weight: 600; }
    .app-dashboard .scroll-hint { bottom: 22px; left: auto; right: 12vw; color: #6c7d78; }
    .app-dashboard .scroll-line { background: #aab8b0; }
    .app-dashboard .play-button { color: var(--ink); }
    .app-dashboard .play-icon { border-color: #9eada6; }
    .explore-section { max-width: none; padding: 54px 8vw 65px; background: #fbfcf9; }
    .section-heading { max-width: 1300px; margin: 0 auto 36px; }
    .section-intro { margin-right: 0; }
    .trip-search { max-width: 1300px; margin: 0 auto 17px; border-color: #d9e0da; box-shadow: 0 9px 20px rgba(16,45,50,.04); }
    .trip-planner-form { display: grid; grid-template-columns: repeat(5, minmax(170px, 1fr)); gap: 12px; align-items: end; }
    .trip-planner-form .search-field { min-height: 86px; }
    .trip-planner-form .search-field input, .trip-planner-form .search-field select {
      width: 100%; min-height: 44px; padding: 10px 12px; border-radius: 12px; border: 1px solid #d8ddd9; background: #fff;
    }
    .trip-planner-form .search-button { min-height: 56px; }
    .search-result {
      max-width: 980px;
      margin: 0 auto 18px;
      padding: 18px 22px;
      border: 1px solid #dfe7df;
      border-radius: 18px;
      background: rgba(255,255,255,.94);
      box-shadow: 0 18px 35px rgba(16,45,50,.09);
      color: #1d2e2b;
      font-size: clamp(1rem, 1.4vw, 1.28rem);
      line-height: 1.6;
      font-weight: 600;
    }
    .destination-grid { display: grid; max-width: 1300px; margin: 0 auto; grid-template-columns: 1.35fr 1fr 1fr; }
    .destination-card { height: 360px; }
    .destination-card img { display: block; width: 100%; height: 100%; object-fit: cover; object-position: center; transition: transform .6s ease; }
    .destination-card:hover img { transform: scale(1.04); }
    body.modal-open { overflow: hidden; }
    .detail-modal { position: fixed; inset: 0; display: none; align-items: center; justify-content: center; background: rgba(17, 24, 21, 0.62); z-index: 1000; padding: 24px; overflow-y: auto; }
    .detail-modal.open { display: flex; }
    .detail-modal-card { width: min(760px, 100%); max-height: min(82vh, 780px); overflow-y: auto; background: #fbfcf9; border-radius: 24px; border: 1px solid rgba(16,45,50,.12); box-shadow: 0 30px 70px rgba(16,45,50,.25); padding: 0; position: relative; }
    .detail-close { position: absolute; top: 16px; right: 16px; width: 38px; height: 38px; border: 0; border-radius: 50%; background: #edf1eb; color: var(--ink); font-size: 1.6rem; cursor: pointer; z-index: 2; }
    .detail-image { width: 100%; height: 320px; object-fit: cover; object-position: center; display: block; border-radius: 24px 24px 0 0; filter: saturate(1.12) contrast(1.08); }
    .detail-content-inner { padding: 26px 28px 22px; }
    .detail-header { margin-bottom: 18px; }
    .detail-header h3 { margin: 10px 0 0; font-size: clamp(2rem, 3vw, 3rem); letter-spacing: -0.05em; }
    .detail-copy { color: #41504d; font-size: 1.02rem; line-height: 1.7; margin: 0 0 20px; }
    .detail-metrics { display: grid; grid-template-columns: repeat(2, minmax(170px, 1fr)); gap: 12px; margin-bottom: 20px; }
    .detail-metrics div { background: #edf2ee; border: 1px solid #dae3db; border-radius: 16px; padding: 14px 16px; }
    .detail-metrics span { display: block; color: #667772; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
    .detail-metrics strong { color: var(--ink); font-size: 1.15rem; }
    .detail-price { margin-top: 8px; padding: 16px 18px; border-radius: 16px; background: linear-gradient(135deg, #f6efe5, #fffaf1); border: 1px solid #f0debb; font-size: 1.2rem; font-weight: 700; color: #2d3d36; }
    .detail-price .pill { display: inline-block; margin-right: 8px; padding: 6px 10px; border-radius: 999px; background: rgba(183,129,46,.16); color: #7a5819; font-size: 0.7rem; letter-spacing: 0.06em; text-transform: uppercase; }
    .card-content h3 { font-size: clamp(1.8rem, 2.8vw, 2.7rem); }
    .card-description { margin: -5px 0 0; max-width: 190px; color: rgba(255,255,255,.82); font-size: 11px; line-height: 1.35; }
    .trust-strip { grid-template-columns: repeat(3, 1fr) 1.3fr; padding: 25px 8vw; background: #eef1ed; border-top: 1px solid #dce2dc; border-bottom: 1px solid #dce2dc; }
    .trust-strip div { color: var(--ink); border-color: #cfd8d1; }
    .trust-strip span { color: #64746f; }
    .trust-strip p { color: #bd8030; }
    .trust-strip p span { color: var(--ink); }
    footer { background: #fbfcf9; }
    @media (max-width: 760px) {
      .site-header { min-height: 68px; }
      .hero.app-dashboard { padding: 38px 8vw 52px; }
      .app-dashboard h1 { font-size: clamp(2.8rem, 13vw, 4rem); }
      .app-dashboard .hero-note { top: auto; bottom: 22px; right: 8vw; }
      .app-dashboard .scroll-hint { left: 8vw; right: auto; bottom: 23px; }
      .explore-section { padding: 54px 6vw 65px; }
      .destination-card, .featured-card { height: 310px; }
      .trust-strip { padding: 28px 8vw; }
    }
  </style>
</head>
<body>
  <header class="site-header">
    <a class="brand" href="#top" aria-label="Himalaya home">
      <span class="brand-mark">H</span>
      <span>himalaya<span class="brand-dot">.</span></span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Main navigation">
      <a class="active" href="#explore">Explore</a>
      <a href="#how-it-works">My trips</a>
      <a href="#stories">Profile</a>
    </nav>
    <div class="header-actions">
      <div class="language-picker">
        <button class="language-button" id="language-button" type="button" aria-label="Select language" aria-haspopup="true" aria-expanded="false"><span id="current-language">EN</span> <span>⌄</span></button>
        <div class="language-menu" id="language-menu" role="menu">
          <button type="button" role="menuitem" data-language="en">English</button>
          <button type="button" role="menuitem" data-language="ja">日本語</button>
          <button type="button" role="menuitem" data-language="zh">中文</button>
          <button type="button" role="menuitem" data-language="ko">한국어</button>
        </div>
      </div>
      <button class="sign-in" id="dashboard-signout" type="button">Log out</button>
    </div>
  </header>

  <main id="top">
    <section class="hero app-dashboard" aria-labelledby="hero-title">
      <div class="hero-content">
        <p class="eyebrow"><span class="eyebrow-line"></span> <span data-i18n="heroEyebrow">Your trip dashboard</span></p>
        <h1 id="hero-title" data-i18n-html="heroTitle">Welcome back,<br /><em>{{ user_name }}</em></h1>
        <p class="hero-copy" data-i18n="heroCopy">From quiet mountain villages to wild jungle trails, discover a journey shaped around the way you want to travel.</p>
        <div class="hero-buttons">
          <a class="primary-button" href="#explore"><span data-i18n="startExploring">Plan a new trip</span> <span>+</span></a>
          <button class="play-button" type="button" aria-label="View saved trips" data-i18n-aria="watchStory"><span class="play-icon">⌑</span> <span data-i18n="seeStory">Saved trips</span></button>
        </div>
      </div>
      <div class="hero-note">
        <span class="hero-note-icon">✦</span>
        <span data-i18n-html="heroNote">Kathmandu<br /><strong>18°C · Clear</strong></span>
      </div>
      <div class="scroll-hint"><span data-i18n="scrollToExplore">3 saved trips</span><span class="scroll-line"></span></div>
    </section>

    <section class="explore-section" id="explore" aria-labelledby="explore-title">
      <div class="section-heading">
        <div>
          <p class="eyebrow dark-eyebrow"><span class="eyebrow-line"></span> <span data-i18n="curatedForYou">AI recommendations</span></p>
          <h2 id="explore-title" data-i18n-html="exploreTitle">Explore Nepal<br /><em>your way.</em></h2>
        </div>
        <p class="section-intro" data-i18n="sectionIntro">Routes matched to your time, energy, and the kind of stories you want to bring home.</p>
      </div>

      <form class="trip-search trip-planner-form" id="dashboard-search">
        <label class="search-field destination-field">
          <span class="field-icon">↗</span>
          <span><small id="from-label">From</small>
            <select id="from-input">
              <option value="">Select country</option>
              <option value="Japan">Japan</option>
              <option value="Korea">Korea</option>
              <option value="Australia">Australia</option>
              <option value="America">America</option>
              <option value="China">China</option>
            </select>
          </span>
        </label>
        <label class="search-field destination-field">
          <span class="field-icon">⌖</span>
          <span><small id="to-label">To</small><select id="to-input"><option value="">Select place</option></select></span>
        </label>
        <label class="search-field">
          <span class="field-icon">🗓</span>
          <span><small id="departure-label">Departure</small><input id="departure-date" type="date" min="" /></span>
        </label>
        <label class="search-field">
          <span class="field-icon">↩</span>
          <span><small id="return-label">Return</small><input id="return-date" type="date" min="" /></span>
        </label>
        <button class="search-button" type="submit"><span id="find-trips-button-label">Search</span> <span>→</span></button>
      </form>
      <p class="search-result" id="search-result" aria-live="polite"></p>

      <div class="detail-modal" id="destination-modal" aria-hidden="true">
        <div class="detail-modal-card" role="dialog" aria-modal="true" aria-labelledby="detail-title">
          <button class="detail-close" id="detail-close" type="button" aria-label="Close popup">×</button>
          <div id="detail-content"></div>
        </div>
      </div>

      <div class="destination-grid" id="destination-grid"></div>
    </section>

    <section class="trust-strip" id="how-it-works">
      <div><strong>01</strong><span data-i18n-html="stepOne">Pick a place<br />or feeling</span></div>
      <div><strong>02</strong><span data-i18n-html="stepTwo">Shape your<br />perfect route</span></div>
      <div><strong>03</strong><span data-i18n-html="stepThree">Keep it<br />all together</span></div>
      <p data-i18n-html="trustMessage">Your trip, in one place<br /><span>ready when you are.</span></p>
    </section>
  </main>

  <footer id="stories"><span>© 2025 Himalaya</span><span data-i18n="footerTagline">Travel deeper. Feel more.</span></footer>

  <script>
    const destinations = {{ destinations|tojson|safe }};
    const translations = {
      en: { label: 'EN', heroEyebrow: 'Your trip dashboard', heroTitle: 'Welcome back,<br /><em>{{ user_name }}</em>', heroCopy: 'From quiet mountain villages to wild jungle trails, discover a journey shaped around the way you want to travel.', startExploring: 'Plan a new trip', seeStory: 'Saved trips', scrollToExplore: '3 saved trips', curatedForYou: 'AI recommendations', exploreTitle: 'Explore Nepal<br /><em>your way.</em>', sectionIntro: 'Routes matched to your time, energy, and the kind of stories you want to bring home.', dreamingOf: "I'm dreaming of", destinationPlaceholder: 'A place or experience', travelMood: 'My travel mood', moodAll: 'Any kind of adventure', moodMountains: 'Mountain air', moodCulture: 'Culture & calm', moodWild: 'Wild escapes', findMyTrip: 'Find my trip', heroNote: 'Kathmandu<br /><strong>18°C · Clear</strong>', stepOne: 'Pick a place<br />or feeling', stepTwo: 'Shape your<br />perfect route', stepThree: 'Keep it<br />all together', trustMessage: 'Your trip, in one place<br /><span>ready when you are.</span>', footerTagline: 'Travel deeper. Feel more.', saveThis: 'Save this trip', removeSaved: 'Remove from saved trips', emptyState: 'No journeys found yet. Try “mountain”, “Pokhara”, or choose another mood.', fromLabel: 'From', toLabel: 'To', departureLabel: 'Departure', returnLabel: 'Return', selectCountry: 'Select country', selectPlace: 'Select place', findTrips: 'Search', anyCountry: 'Any country', noTrips: 'No trips found for', placesFound: 'places found from', depart: 'Depart', returnText: 'Return', daysLabel: 'days', totalLabel: 'Total', flightLabel: 'Flight', tripCostLabel: 'trip costs', flexibleLabel: 'Flexible', adventureLabel: 'Adventure', dayShortLabel: '/day' },
      ja: { label: 'JA', heroEyebrow: 'あなたの旅ダッシュボード', heroTitle: 'お帰りなさい、<br /><em>{{ user_name }}</em>', heroCopy: '静かな山村から野生のジャングルまで、あなたらしい旅を形にしましょう。', startExploring: '新しい旅を計画', seeStory: '保存した旅', scrollToExplore: '保存した旅 3件', curatedForYou: 'AIおすすめ', exploreTitle: 'ネパールを探す<br /><em>あなたらしく。</em>', sectionIntro: '時間、体力、持ち帰りたい物語に合わせたルートをご提案します。', dreamingOf: '夢見ている場所', destinationPlaceholder: '場所や体験を入力', travelMood: '旅の気分', moodAll: 'すべての冒険', moodMountains: '山の空気', moodCulture: '文化と癒やし', moodWild: '野生の旅', findMyTrip: '旅を見つける', heroNote: 'カトマンズ<br /><strong>18°C · 晴れ</strong>', stepOne: '場所や気分を<br />選ぶ', stepTwo: 'ぴったりのルートを<br />つくる', stepThree: '旅をひとつに<br />まとめる', trustMessage: '旅をひとつの場所に<br /><span>いつでも準備万端。</span>', footerTagline: '深く旅して、もっと感じる。', saveThis: 'この旅を保存', removeSaved: '保存済みから削除', emptyState: '旅が見つかりません。「山」「ポカラ」または別の気分を試してください。', fromLabel: '出発地', toLabel: '目的地', departureLabel: '出発日', returnLabel: '帰国日', selectCountry: '国を選択', selectPlace: '場所を選択', findTrips: '検索', anyCountry: 'どの国でも', noTrips: '該当の旅程が見つかりません', placesFound: '件の候補が見つかりました', depart: '出発', returnText: '帰着', daysLabel: '日', totalLabel: '合計', flightLabel: '航空券', tripCostLabel: '旅行費用', flexibleLabel: '柔軟', adventureLabel: '冒険', dayShortLabel: '/日' },
      zh: { label: 'ZH', heroEyebrow: '你的旅行仪表盘', heroTitle: '欢迎回来，<br /><em>{{ user_name }}</em>', heroCopy: '从安静的山村到荒野丛林，按你想要的方式规划旅行。', startExploring: '规划新旅程', seeStory: '已保存旅程', scrollToExplore: '已保存 3 段旅程', curatedForYou: 'AI 为你推荐', exploreTitle: '探索尼泊尔<br /><em>找到你的方式。</em>', sectionIntro: '根据你的时间、体力和想带回家的故事，为你匹配路线。', dreamingOf: '我向往的地方', destinationPlaceholder: '地点或体验', travelMood: '我的旅行心情', moodAll: '任何冒险', moodMountains: '山间清风', moodCulture: '文化与宁静', moodWild: '野外探索', findMyTrip: '寻找我的旅程', heroNote: '加德满都<br /><strong>18°C · 晴</strong>', stepOne: '选择地点<br />或心情', stepTwo: '规划你的<br />完美路线', stepThree: '把旅程<br />放在一起', trustMessage: '让旅程集中在<br /><span>一个随时可用的地方。</span>', footerTagline: '深入旅行，感受更多。', saveThis: '保存这段旅程', removeSaved: '从已保存旅程中移除', emptyState: '暂时没有找到旅程。试试“山脉”“博卡拉”，或选择另一种心情。', fromLabel: '出发地', toLabel: '目的地', departureLabel: '出发日', returnLabel: '返程日', selectCountry: '选择国家', selectPlace: '选择地点', findTrips: '搜索', anyCountry: '任何国家', noTrips: '未找到合适行程', placesFound: '个目的地已为您筛选', depart: '出发', returnText: '返回', daysLabel: '天', totalLabel: '总价', flightLabel: '机票', tripCostLabel: '旅行费用', flexibleLabel: '灵活', adventureLabel: '探险', dayShortLabel: '/天' },
      ko: { label: 'KO', heroEyebrow: '나의 여행 대시보드', heroTitle: '다시 오셨네요,<br /><em>{{ user_name }}</em>', heroCopy: '조용한 산마을에서 야생 정글까지, 당신이 원하는 방식으로 여행을 설계해보세요.', startExploring: '새 여행 계획하기', seeStory: '저장한 여행', scrollToExplore: '저장한 여행 3개', curatedForYou: 'AI 추천', exploreTitle: '네팔 탐색하기<br /><em>나만의 방식으로.</em>', sectionIntro: '시간과 체력, 집으로 가져오고 싶은 이야기에 맞는 루트를 추천해드려요.', dreamingOf: '꿈꾸는 여행지', destinationPlaceholder: '장소 또는 경험', travelMood: '나의 여행 기분', moodAll: '어떤 모험이든', moodMountains: '산의 공기', moodCulture: '문화와 휴식', moodWild: '야생 속으로', findMyTrip: '내 여행 찾기', heroNote: '카트만두<br /><strong>18°C · 맑음</strong>', stepOne: '장소나 기분을<br />선택하세요', stepTwo: '나만의 완벽한<br />루트를 만드세요', stepThree: '여행을 한곳에<br />모아보세요', trustMessage: '여행을 한곳에 모아<br /><span>언제든 준비하세요.</span>', footerTagline: '더 깊이 여행하고, 더 많이 느껴보세요.', saveThis: '이 여행 저장', removeSaved: '저장한 여행에서 삭제', emptyState: '아직 여행을 찾지 못했어요. “산”, “포카라” 또는 다른 기분을 선택해 보세요.', fromLabel: '출발지', toLabel: '도착지', departureLabel: '출발일', returnLabel: '복귀일', selectCountry: '국가 선택', selectPlace: '장소 선택', findTrips: '검색', anyCountry: '모든 국가', noTrips: '조건에 맞는 여행이 없습니다', placesFound: '개의 여행지를 찾았습니다', depart: '출발', returnText: '복귀', daysLabel: '일', totalLabel: '총액', flightLabel: '항공권', tripCostLabel: '여행 경비', flexibleLabel: '유연함', adventureLabel: '모험', dayShortLabel: '/일' }
    };

    const languageButton = document.getElementById('language-button');
    const languageMenu = document.getElementById('language-menu');
    const currentLanguageLabel = document.getElementById('current-language');
    let currentLanguage = localStorage.getItem('himalaya-language') || 'en';

    function updateTexts(language) {
      const value = translations[language] || translations.en;
      currentLanguageLabel.textContent = value.label;
      document.querySelectorAll('[data-i18n]').forEach((node) => {
        if (value[node.dataset.i18n]) node.textContent = value[node.dataset.i18n];
      });
      document.querySelectorAll('[data-i18n-html]').forEach((node) => {
        if (value[node.dataset.i18nHtml]) node.innerHTML = value[node.dataset.i18nHtml];
      });
      document.querySelectorAll('[data-i18n-placeholder]').forEach((node) => {
        if (value[node.dataset.i18nPlaceholder]) node.placeholder = value[node.dataset.i18nPlaceholder];
      });
      document.querySelectorAll('[data-i18n-aria]').forEach((node) => {
        if (value[node.dataset.i18nAria]) node.setAttribute('aria-label', value[node.dataset.i18nAria]);
      });
      const heroTitle = document.getElementById('hero-title');
      if (heroTitle) heroTitle.innerHTML = value.heroTitle.replace('{{ user_name }}', '{{ user_name }}');

      const destinationInput = document.getElementById('destination-input');
      if (destinationInput) destinationInput.placeholder = value.destinationPlaceholder;

      const moodSelect = document.getElementById('mood-select');
      if (moodSelect) moodSelect.selectedIndex = 0;

      localStorage.setItem('himalaya-language', language);
    }

    languageButton.addEventListener('click', () => languageMenu.classList.toggle('open'));
    languageMenu.querySelectorAll('button').forEach((button) => {
      button.addEventListener('click', () => {
        currentLanguage = button.dataset.language;
        updateTexts(currentLanguage);
        languageMenu.classList.remove('open');
      });
    });

    const destinationGrid = document.getElementById('destination-grid');
    const fromInput = document.getElementById('from-input');
    const toInput = document.getElementById('to-input');
    const departureDateInput = document.getElementById('departure-date');
    const returnDateInput = document.getElementById('return-date');
    const searchResult = document.getElementById('search-result');
    const detailModal = document.getElementById('destination-modal');
    const detailContent = document.getElementById('detail-content');
    const detailClose = document.getElementById('detail-close');

    function closeDestinationModal() {
      detailModal.classList.remove('open');
      detailModal.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('modal-open');
    }

    function openDestinationPopup(destination, tripCost, fromCountry, departureDate, returnDate) {
      if (!destination) {
        closeDestinationModal();
        return;
      }

      const lang = translations[currentLanguage];
      const departureLabel = departureDate ? departureDate : lang.depart;
      const returnLabel = returnDate ? returnDate : lang.returnText;
      const formatValue = (value) => `¥${formatCurrency(value)}`;

      detailContent.innerHTML = `
        <img class="detail-image" src="${destination.image_url || destination.image || ''}" alt="${destination.name}" />
        <div class="detail-content-inner">
          <div class="detail-header">
            <span class="card-tag">${destination.region}</span>
            <h3 id="detail-title">${destination.name}</h3>
          </div>
          <p class="detail-copy">${getLocalizedDestinationText(destination, currentLanguage)}</p>
          <div class="detail-metrics">
            <div>
              <span>${lang.fromLabel}</span>
              <strong>${fromCountry || lang.anyCountry}</strong>
            </div>
            <div>
              <span>${lang.toLabel}</span>
              <strong>${destination.name}</strong>
            </div>
            <div>
              <span>${lang.departureLabel}</span>
              <strong>${departureLabel}</strong>
            </div>
            <div>
              <span>${lang.returnLabel}</span>
              <strong>${returnLabel}</strong>
            </div>
          </div>
          <div class="detail-price"><span class="pill">${lang.totalLabel}</span> ${formatValue(tripCost ? tripCost.totalCost : 0)}</div>
          <div class="detail-metrics" style="margin-top: 14px;">
            <div>
              <span>${lang.flightLabel}</span>
              <strong>${formatValue(tripCost ? tripCost.airfare : 0)}</strong>
            </div>
            <div>
              <span>${lang.tripCostLabel}</span>
              <strong>${formatValue(tripCost ? tripCost.localExpenses : 0)}</strong>
            </div>
          </div>
        </div>
      `;

      detailModal.classList.add('open');
      detailModal.setAttribute('aria-hidden', 'false');
      document.body.classList.add('modal-open');
    }

    detailClose.addEventListener('click', closeDestinationModal);
    detailModal.addEventListener('click', (event) => {
      if (event.target === detailModal) closeDestinationModal();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && detailModal.classList.contains('open')) {
        closeDestinationModal();
      }
    });

    function formatDateInput(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }

    function syncDateConstraints() {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const todayValue = formatDateInput(today);
      departureDateInput.min = todayValue;
      returnDateInput.min = todayValue;

      if (departureDateInput.value && new Date(departureDateInput.value) < today) {
        departureDateInput.value = '';
      }
      if (returnDateInput.value && new Date(returnDateInput.value) < today) {
        returnDateInput.value = '';
      }

      if (departureDateInput.value) {
        const departureDate = new Date(`${departureDateInput.value}T00:00:00`);
        returnDateInput.min = formatDateInput(departureDate);
        if (returnDateInput.value && new Date(`${returnDateInput.value}T00:00:00`) < departureDate) {
          returnDateInput.value = departureDateInput.value;
        }
      }
    }

    const placeOptions = [...new Set(destinations.map((destination) => destination.name))].sort();
    placeOptions.forEach((place) => {
      const option = document.createElement('option');
      option.value = place;
      option.textContent = place;
      toInput.appendChild(option);
    });

    const countryFlightBaseJpy = {
      Japan: 98000,
      Korea: 76000,
      China: 68000,
      Australia: 142000,
      America: 188000,
      default: 110000
    };

    const destinationRegionFactor = {
      Central: 1.0,
      Eastern: 1.08,
      Western: 1.12,
      Northern: 1.2,
      Southern: 0.96
    };

    function getTripDays(departureDate, returnDate) {
      if (!departureDate || !returnDate) {
        return 1;
      }

      const departure = new Date(`${departureDate}T00:00:00`);
      const returnDay = new Date(`${returnDate}T00:00:00`);
      const diffDays = Math.round((returnDay - departure) / 86400000) + 1;
      return Math.max(1, diffDays);
    }

    function getTripCostEstimate(destination, fromCountry, departureDate, returnDate) {
      if (!destination) {
        return null;
      }

      const tripDays = getTripDays(departureDate, returnDate);
      const airfare = Math.round((countryFlightBaseJpy[fromCountry] || countryFlightBaseJpy.default) * (destinationRegionFactor[destination.region] || 1));
      const localExpenses = Math.round((destination.daily_cost || 0) * tripDays * 150);
      const totalCost = airfare + localExpenses;

      return {
        tripDays,
        airfare,
        localExpenses,
        totalCost,
      };
    }

    function formatCurrency(value) {
      return new Intl.NumberFormat('ja-JP').format(value);
    }

    function getLocalizedDestinationText(destination, language) {
      const description = destination && destination.description ? destination.description : 'Explore this destination.';
      const translationMap = {
        en: {
          "Tea gardens, cool hills, and a calm countryside rhythm.": "Tea gardens, cool hills, and a calm countryside rhythm.",
          "Historic temples, lively streets, and rich local cuisine.": "Historic temples, lively streets, and rich local cuisine.",
          "A lakeside escape framed by snow-capped mountains.": "A lakeside escape framed by snow-capped mountains.",
          "A classic hill town with heritage homes and mountain views.": "A classic hill town with heritage homes and mountain views.",
          "Wildlife safaris and rich wildlife in Nepal's lowlands.": "Wildlife safaris and rich wildlife in Nepal's lowlands.",
          "Buddhist heritage and peaceful spiritual experiences.": "Buddhist heritage and peaceful spiritual experiences.",
          "Ancient temples and a rich Mithila cultural tradition.": "Ancient temples and a rich Mithila cultural tradition.",
          "A legendary Himalayan trek with unforgettable glacier views.": "A legendary Himalayan trek with unforgettable glacier views.",
          "A dramatic Himalayan range with sweeping mountain routes.": "A dramatic Himalayan range with sweeping mountain routes.",
          "An arid highland region with strong Tibetan heritage.": "An arid highland region with strong Tibetan heritage.",
          "A quieter Himalayan trekking experience with valleys and ridges.": "A quieter Himalayan trekking experience with valleys and ridges.",
          "A remote and dramatic Himalayan circuit with wide-open views.": "A remote and dramatic Himalayan circuit with wide-open views.",
          "A protected park with rich birdlife and jungle landscapes.": "A protected park with rich birdlife and jungle landscapes.",
          "A nearby hill station for sunrise views and easy escapes.": "A nearby hill station for sunrise views and easy escapes.",
          "A secluded alpine lake surrounded by wild mountain views.": "A secluded alpine lake surrounded by wild mountain views.",
          "Temple courtyards, artisan workshops, and Newari heritage.": "Temple courtyards, artisan workshops, and Newari heritage.",
          "Historic hill town life with views, heritage, and warmth.": "Historic hill town life with views, heritage, and warmth.",
          "Remote Himalayan scenery with an expansive and wild feel.": "Remote Himalayan scenery with an expansive and wild feel.",
          "Wetland birds, wildlife, and quiet river landscapes.": "Wetland birds, wildlife, and quiet river landscapes."
        },
        ja: {
          "Tea gardens, cool hills, and a calm countryside rhythm.": "茶園、涼しい丘、落ち着いた田園のリズム。",
          "Historic temples, lively streets, and rich local cuisine.": "歴史的な寺院、賑やかな通り、豊かな地元料理。",
          "A lakeside escape framed by snow-capped mountains.": "雪を頂いた山々に囲まれた湖畔の安らぎ。",
          "A classic hill town with heritage homes and mountain views.": "歴史ある家々と山の景色が広がる古き良き丘の町。",
          "Wildlife safaris and rich wildlife in Nepal's lowlands.": "ネパール低地の野生動物サファリと豊かな自然。",
          "Buddhist heritage and peaceful spiritual experiences.": "仏教遺産と静かな精神的体験。",
          "Ancient temples and a rich Mithila cultural tradition.": "古代寺院と豊かなミティラ文化の伝統。",
          "A legendary Himalayan trek with unforgettable glacier views.": "忘れられない氷河の景色が広がる伝説的なヒマラヤ登山。",
          "A dramatic Himalayan range with sweeping mountain routes.": "広大な山道が続くドラマティックなヒマラヤ。",
          "An arid highland region with strong Tibetan heritage.": "強いチベット文化を持つ乾いた高地の地域。",
          "A quieter Himalayan trekking experience with valleys and ridges.": "谷と尾根が続く、静かなヒマラヤのトレッキング体験。",
          "A remote and dramatic Himalayan circuit with wide-open views.": "開けた景色が広がる、遠く離れたドラマティックな山岳ルート。",
          "A protected park with rich birdlife and jungle landscapes.": "豊かな鳥類とジャングルの風景が広がる保護地域。",
          "A nearby hill station for sunrise views and easy escapes.": "日の出の景色を楽しめる、身近なヒルステーション。",
          "A secluded alpine lake surrounded by wild mountain views.": "荒々しい山々に囲まれた秘境の高山湖。",
          "Temple courtyards, artisan workshops, and Newari heritage.": "寺院の中庭、職人の工房、ネワール文化の遺産。",
          "Historic hill town life with views, heritage, and warmth.": "景色、歴史、温かさがあふれる古い丘の町。",
          "Remote Himalayan scenery with an expansive and wild feel.": "広がる自然と荒々しい雰囲気の遠隔地ヒマラヤ。",
          "Wetland birds, wildlife, and quiet river landscapes.": "湿地の鳥たち、野生動物、静かな川の風景。"
        }
      };

      const localized = translationMap[language] && translationMap[language][description]
        ? translationMap[language][description]
        : description;
      return localized || 'Explore this destination.';
    }

    function formatBestForTags(bestFor, language) {
      const labels = {
        en: { tea_gardens: 'tea_gardens', peaceful_hills: 'peaceful_hills', culture: 'culture', nature: 'nature', heritage: 'heritage', mountains: 'mountains', trekking: 'trekking', adventure: 'adventure', wildlife: 'wildlife', city: 'city', history: 'history', short_visit: 'short visit', quiet_trek: 'quiet trek', scenic_views: 'scenic views', mountain_views: 'mountain views', heritage_homes: 'heritage homes', local_culture: 'local culture', birding: 'birding', lake_views: 'lake views', remote_trip: 'remote trip', food: 'food', religion: 'religion', photography: 'photography' },
        ja: { tea_gardens: '茶園', peaceful_hills: '穏やかな丘', culture: '文化', nature: '自然', heritage: '遺産', mountains: '山', trekking: 'トレッキング', adventure: '冒険', wildlife: '野生動物', city: '都市', history: '歴史', short_visit: '短時間旅行', quiet_trek: '静かなトレッキング', scenic_views: '景色', mountain_views: '山の景色', heritage_homes: '歴史的な家', local_culture: '地域文化', birding: 'バードウォッチング', lake_views: '湖の景色', remote_trip: '秘境旅行', food: '食事', religion: '宗教', photography: '写真' }
      };

      const map = labels[language] || labels.en;
      const items = Array.isArray(bestFor) ? bestFor : [];
      return items.map((item) => (map[item] || item.replace(/_/g, ' '))).join(', ');
    }

    function renderDestinations(options = {}) {
      const { openPopup = false } = options;
      const fromCountry = fromInput.value;
      const selectedPlace = toInput.value;
      const departureDate = departureDateInput.value;
      const returnDate = returnDateInput.value;

      const matches = destinations.filter((destination) => {
        const haystack = [destination.name, destination.region, destination.description, ...(destination.interests || []), ...(destination.best_for || [])].join(' ').toLowerCase();
        const fromMatch = !fromCountry || fromCountry === 'Select country' || true;
        const toMatch = !selectedPlace || destination.name === selectedPlace || destination.region === selectedPlace;
        const dateMatch = !departureDate || !returnDate || new Date(returnDate) >= new Date(departureDate);

        return fromMatch && toMatch && dateMatch && haystack.length > 0;
      });

      destinationGrid.innerHTML = '';
      destinationGrid.style.display = 'none';

      if (!matches.length) {
        closeDestinationModal();
        const where = selectedPlace || 'Nepal';
        searchResult.textContent = `No trips found for ${where}`;
        return;
      }

      const fromLabel = fromCountry || 'Any country';
      const toLabel = selectedPlace || 'Nepal';
      const departureText = departureDate ? ` · ${translations[currentLanguage].depart} ${departureDate}` : '';
      const returnText = returnDate ? ` · ${translations[currentLanguage].returnText} ${returnDate}` : '';
      const selectedDestination = selectedPlace ? (matches.find((destination) => destination.name === selectedPlace) || matches[0]) : matches[0];
      const tripCost = getTripCostEstimate(selectedDestination, fromCountry || 'Japan', departureDate || '2026-09-14', returnDate || '2026-09-19');
      const lang = translations[currentLanguage];

      destinationGrid.style.display = 'grid';
      destinationGrid.innerHTML = matches.slice(0, 6).map((destination) => {
        const estimate = getTripCostEstimate(destination, fromCountry || 'Japan', departureDate || '2026-09-14', returnDate || '2026-09-19');
        const image = destination.image_url || destination.image || 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80';
        const totalText = estimate ? `¥${formatCurrency(estimate.totalCost)}` : '¥0';
        return `
          <article class="destination-card" data-name="${destination.name}" tabindex="0" aria-label="${destination.name}">
            <img src="${image}" alt="${destination.name}" loading="lazy" />
            <div class="card-overlay"></div>
            <div class="card-content">
              <div class="card-topline">
                <span class="card-tag">${destination.region}</span>
                <button class="save-button" type="button" aria-label="Save ${destination.name}">♡</button>
              </div>
              <div>
                <h3>${destination.name}</h3>
                <p class="card-description">${getLocalizedDestinationText(destination, currentLanguage)}</p>
                <div class="card-meta">
                  <span>${lang.totalLabel} ${totalText}</span>
                  <span>${estimate ? `${estimate.tripDays} ${lang.daysLabel}` : ''}</span>
                </div>
              </div>
            </div>
          </article>
        `;
      }).join('');

      destinationGrid.querySelectorAll('.destination-card').forEach((card) => {
        card.addEventListener('click', () => {
          const name = card.dataset.name;
          const destination = destinations.find((item) => item.name === name);
          const estimate = destination ? getTripCostEstimate(destination, fromCountry || 'Japan', departureDate || '2026-09-14', returnDate || '2026-09-19') : null;
          if (destination && estimate) {
            openDestinationPopup(destination, estimate, fromCountry || 'Japan', departureDate || '2026-09-14', returnDate || '2026-09-19');
          }
        });
        card.addEventListener('keydown', (event) => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            card.click();
          }
        });
      });

      if (selectedPlace && fromCountry && tripCost && openPopup) {
        openDestinationPopup(selectedDestination, tripCost, fromCountry, departureDate || '2026-09-14', returnDate || '2026-09-19');
      } else {
        closeDestinationModal();
      }

      if (selectedPlace && fromCountry && tripCost && openPopup) {
        searchResult.textContent = `${lang.fromLabel} ${fromLabel} ${lang.toLabel.toLowerCase()} ${selectedDestination.name} • ${tripCost.tripDays} ${lang.daysLabel} • ${lang.totalLabel} ¥${formatCurrency(tripCost.totalCost)} (${lang.flightLabel} ¥${formatCurrency(tripCost.airfare)} + ${lang.tripCostLabel} ¥${formatCurrency(tripCost.localExpenses)})${departureText}${returnText}`;
      } else {
        searchResult.textContent = `${matches.length} ${lang.placesFound} ${fromLabel} ${lang.toLabel.toLowerCase()} ${toLabel}${departureText}${returnText}`;
      }
    }

    document.getElementById('dashboard-search').addEventListener('submit', (event) => {
      event.preventDefault();
      renderDestinations({ openPopup: true });
    });

    fromInput.addEventListener('change', () => renderDestinations({ openPopup: false }));
    toInput.addEventListener('change', () => renderDestinations({ openPopup: false }));
    departureDateInput.addEventListener('change', () => {
      syncDateConstraints();
      renderDestinations();
    });
    returnDateInput.addEventListener('change', () => {
      syncDateConstraints();
      renderDestinations();
    });

    document.getElementById('dashboard-signout').addEventListener('click', async () => {
      await fetch('/api/signout', { method: 'POST' });
      window.location.href = '/signin.html';
    });

    updateTexts(currentLanguage);
    syncDateConstraints();
    renderDestinations();
  </script>
</body>
</html>
"""


@pages.get("/dashboard")
def dashboard_page():
    if "user_id" not in session:
        return redirect("/signin.html")
    return render_template_string(
        DASHBOARD_HTML,
        user_name=session.get("user_name", "Traveler"),
        destinations=DESTINATIONS,
    )


@pages.get("/<path:filename>")
def public_file(filename):
    return send_from_directory(current_app.config["PROJECT_ROOT"], filename)


def validate_signup(payload):
    full_name = payload.get("fullName", "").strip()
    username = payload.get("username", "").strip().lower()
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")
    travel_interest = payload.get("travelInterest", "")

    if not full_name:
        return None, "Please enter your name."
    if not username or not USERNAME_PATTERN.match(username):
        return None, "Please choose a username with 3-30 letters, numbers, dots, underscores, or dashes."
    if not EMAIL_PATTERN.match(email):
        return None, "Please enter a valid email address."
    if len(password) < 8:
        return None, "Your password must be at least 8 characters."
    if travel_interest not in ALLOWED_INTERESTS:
        return None, "Please choose a travel style."
    return (full_name, username, email, password, travel_interest), None


@auth_api.post("/signup")
def signup():
    payload = request.get_json(silent=True) or request.form
    values, error = validate_signup(payload)
    if error:
        return jsonify({"error": error}), 400

    full_name, username, email, password, travel_interest = values
    if find_user_by_email(email) is not None:
        return jsonify({"error": "An account with that email already exists."}), 409
    if find_user_by_username(username) is not None:
        return jsonify({"error": "This username is already taken."}), 409

    user = create_user(full_name, username, email, password, travel_interest)
    session.clear()
    session["user_id"] = user.id
    session["user_name"] = user.full_name
    return jsonify({"message": "Account created successfully.", "user": {"name": user.full_name, "username": user.username, "email": user.email}}), 201


@auth_api.post("/signin")
def signin():
    payload = request.get_json(silent=True) or request.form
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")
    user = authenticate_user(email, password)
    if user is None:
        return jsonify({"error": "Email or password is incorrect."}), 401

    session.clear()
    session["user_id"] = user.id
    session["user_name"] = user.full_name
    return jsonify({"message": f"Welcome back, {user.full_name}.", "user": {"name": user.full_name, "email": user.email}})


@auth_api.post("/signout")
def signout():
    session.clear()
    return jsonify({"message": "You have been signed out."})


@auth_api.get("/me")
def current_user():
    if "user_id" not in session:
        return jsonify({"user": None})
    return jsonify({"user": {"id": session["user_id"], "name": session["user_name"]}})
