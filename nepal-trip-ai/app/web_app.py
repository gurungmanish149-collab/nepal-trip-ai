import os
import sys

if __package__ in (None, ""):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from flask import Flask, redirect, render_template_string, request, send_from_directory, session

from app.data import DESTINATIONS
from app.database import init_app, init_database
from app.planner import TravelPlanner
from app.routes import auth_api

app = Flask(__name__, static_folder="static", static_url_path="/static")
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-change-this-secret"),
    DATABASE=os.path.join(project_root, "instance", "himalaya.sqlite3"),
    PROJECT_ROOT=project_root,
)
init_app(app)
app.register_blueprint(auth_api, url_prefix="/api")
with app.app_context():
    init_database()
planner = TravelPlanner()

TRANSLATIONS = {
    "en": {
        "title": "NepalTrip AI",
        "subtitle": "Smart Nepal Travel Planner",
        "trip_days": "Days",
        "budget": "Budget (NPR)",
        "region": "Region",
        "interests": "Interest",
        "season": "Season",
        "generate": "Generate Itinerary",
        "map_view": "Map View",
        "details": "Destination Details",
        "select": "Select",
        "placeholder": "Culture / Food / Trekking / Nature / Adventure / History",
        "flight": "Travel Preferences",
        "backend": "Python Backend",
        "database": "Destination Database",
        "route": "Route / Budget",
        "ai": "AI Itinerary",
        "map": "Map + Daily Schedule",
        "total": "Estimated total",
        "select_marker": "Select a destination marker to view its details.",
        "trip_suggestions": "Trip Suggestions",
        "daily_cost": "Daily cost",
        "best_for": "Best for",
        "language": "Language",
        "region_any": "All",
        "region_central": "Central",
        "region_western": "Western",
        "region_eastern": "Eastern",
        "region_southern": "Southern",
        "region_northern": "Northern",
        "season_spring": "Spring",
        "season_summer": "Summer",
        "season_autumn": "Autumn",
        "season_winter": "Winter",
        "season_any": "All"
    },
    "ja": {
        "title": "ネパール旅行AI",
        "subtitle": "スマートなネパール旅行プランナー",
        "trip_days": "旅行日数",
        "budget": "予算（USD）",
        "region": "地域",
        "interests": "興味",
        "season": "季節",
        "generate": "旅程を生成",
        "map_view": "マップ表示",
        "details": "観光地の詳細",
        "select": "選択",
        "placeholder": "文化, トレッキング, 自然",
        "flight": "旅行の好み",
        "backend": "Pythonバックエンド",
        "database": "観光地データベース",
        "route": "ルート / 予算",
        "ai": "AI旅程",
        "map": "マップ + 日程",
        "total": "総額",
        "select_marker": "マーカーを選択して詳細を表示します。",
        "trip_suggestions": "おすすめ旅程",
        "daily_cost": "1日あたりの費用",
        "best_for": "向いている人",
        "language": "言語",
        "region_any": "すべて",
        "region_central": "中央部",
        "region_western": "西部",
        "region_eastern": "東部",
        "region_southern": "南部",
        "region_northern": "北部",
        "season_spring": "春",
        "season_summer": "夏",
        "season_autumn": "秋",
        "season_winter": "冬",
        "season_any": "すべて"
    },
    "zh": {
        "title": "尼泊尔旅行AI",
        "subtitle": "智能尼泊尔旅行规划师",
        "trip_days": "旅行天数",
        "budget": "预算（USD）",
        "region": "地区",
        "interests": "兴趣",
        "season": "季节",
        "generate": "生成行程",
        "map_view": "地图视图",
        "details": "目的地详情",
        "select": "选择",
        "placeholder": "文化, 徒步, 自然",
        "flight": "旅行偏好",
        "backend": "Python后端",
        "database": "目的地数据库",
        "route": "路线 / 预算",
        "ai": "AI 行程",
        "map": "地图 + 日程",
        "total": "预计总额",
        "select_marker": "请选择目的地标记查看详情。",
        "trip_suggestions": "推荐行程",
        "daily_cost": "每日费用",
        "best_for": "适合人群",
        "language": "语言",
        "region_any": "任何",
        "region_central": "中部",
        "region_western": "西部",
        "region_eastern": "东部",
        "region_southern": "南部",
        "region_northern": "北部",
        "season_spring": "春季",
        "season_summer": "夏季",
        "season_autumn": "秋季",
        "season_winter": "冬季",
        "season_any": "任何"
    },
    "ko": {
        "title": "네팔 여행 AI",
        "subtitle": "스마트 네팔 여행 플래너",
        "trip_days": "여행 일수",
        "budget": "예산 (USD)",
        "region": "지역",
        "interests": "관심사",
        "season": "시즌",
        "generate": "여행 코스 생성",
        "map_view": "지도 보기",
        "details": "여행지 정보",
        "select": "선택",
        "placeholder": "문화, 트레킹, 자연",
        "flight": "여행 선호도",
        "backend": "Python 백엔드",
        "database": "여행지 데이터베이스",
        "route": "경로 / 예산",
        "ai": "AI 추천 일정",
        "map": "지도 + 일정",
        "total": "예상 총액",
        "select_marker": "마커를 선택하면 상세 정보를 볼 수 있습니다.",
        "trip_suggestions": "추천 여행지",
        "daily_cost": "일일 비용",
        "best_for": "추천 대상",
        "language": "언어",
        "region_any": "모든 지역",
        "region_central": "중앙",
        "region_western": "서부",
        "region_eastern": "동부",
        "region_southern": "남부",
        "region_northern": "북부",
        "season_spring": "봄",
        "season_summer": "여름",
        "season_autumn": "가을",
        "season_winter": "겨울",
        "season_any": "모든 시즌"
    }
}


def get_translation(language):
    return TRANSLATIONS.get(language, TRANSLATIONS["en"])


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
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
    .search-result { max-width: 1300px; margin: 0 auto 13px; }
    .destination-grid { max-width: 1300px; margin: 0 auto; grid-template-columns: 1.35fr 1fr 1fr; }
    .destination-card { height: 270px; }
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
          <span class="field-icon">◔</span>
          <span><small id="trip-days-label">Days</small><input id="trip-days" type="number" min="3" max="30" value="3" /></span>
        </label>
        <label class="search-field">
          <span class="field-icon">🗓</span>
          <span><small id="departure-label">Departure</small><input id="departure-date" type="date" min="" /></span>
        </label>
        <label class="search-field">
          <span class="field-icon">↩</span>
          <span><small id="return-label">Return</small><input id="return-date" type="date" min="" /></span>
        </label>
        <button class="search-button" type="submit"><span id="find-trips-button-label">Find trips</span> <span>→</span></button>
      </form>
      <p class="search-result" id="search-result" aria-live="polite"></p>

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
      en: { label: 'EN', heroEyebrow: 'Your trip dashboard', heroTitle: 'Welcome back,<br /><em>{{ user_name }}</em>', heroCopy: 'From quiet mountain villages to wild jungle trails, discover a journey shaped around the way you want to travel.', startExploring: 'Plan a new trip', seeStory: 'Saved trips', scrollToExplore: '3 saved trips', curatedForYou: 'AI recommendations', exploreTitle: 'Explore Nepal<br /><em>your way.</em>', sectionIntro: 'Routes matched to your time, energy, and the kind of stories you want to bring home.', dreamingOf: "I'm dreaming of", destinationPlaceholder: 'A place or experience', travelMood: 'My travel mood', moodAll: 'Any kind of adventure', moodMountains: 'Mountain air', moodCulture: 'Culture & calm', moodWild: 'Wild escapes', findMyTrip: 'Find my trip', heroNote: 'Kathmandu<br /><strong>18°C · Clear</strong>', stepOne: 'Pick a place<br />or feeling', stepTwo: 'Shape your<br />perfect route', stepThree: 'Keep it<br />all together', trustMessage: 'Your trip, in one place<br /><span>ready when you are.</span>', footerTagline: 'Travel deeper. Feel more.', saveThis: 'Save this trip', removeSaved: 'Remove from saved trips', emptyState: 'No journeys found yet. Try “mountain”, “Pokhara”, or choose another mood.', fromLabel: 'From', toLabel: 'To', tripDaysLabel: 'Days', departureLabel: 'Departure', returnLabel: 'Return', selectCountry: 'Select country', selectPlace: 'Select place', findTrips: 'Find trips', anyCountry: 'Any country', noTrips: 'No trips found for', placesFound: 'places found from', depart: 'Depart', returnText: 'Return' },
      ja: { label: 'JA', heroEyebrow: 'あなたの旅ダッシュボード', heroTitle: 'お帰りなさい、<br /><em>{{ user_name }}</em>', heroCopy: '静かな山村から野生のジャングルまで、あなたらしい旅を形にしましょう。', startExploring: '新しい旅を計画', seeStory: '保存した旅', scrollToExplore: '保存した旅 3件', curatedForYou: 'AIおすすめ', exploreTitle: 'ネパールを探す<br /><em>あなたらしく。</em>', sectionIntro: '時間、体力、持ち帰りたい物語に合わせたルートをご提案します。', dreamingOf: '夢見ている場所', destinationPlaceholder: '場所や体験を入力', travelMood: '旅の気分', moodAll: 'すべての冒険', moodMountains: '山の空気', moodCulture: '文化と癒やし', moodWild: '野生の旅', findMyTrip: '旅を見つける', heroNote: 'カトマンズ<br /><strong>18°C · 晴れ</strong>', stepOne: '場所や気分を<br />選ぶ', stepTwo: 'ぴったりのルートを<br />つくる', stepThree: '旅をひとつに<br />まとめる', trustMessage: '旅をひとつの場所に<br /><span>いつでも準備万端。</span>', footerTagline: '深く旅して、もっと感じる。', saveThis: 'この旅を保存', removeSaved: '保存済みから削除', emptyState: '旅が見つかりません。「山」「ポカラ」または別の気分を試してください。', fromLabel: '出発地', toLabel: '目的地', tripDaysLabel: '日数', departureLabel: '出発日', returnLabel: '帰国日', selectCountry: '国を選択', selectPlace: '場所を選択', findTrips: '旅を探す', anyCountry: 'どの国でも', noTrips: '該当の旅程が見つかりません', placesFound: '件の候補が見つかりました', depart: '出発', returnText: '帰着' },
      zh: { label: 'ZH', heroEyebrow: '你的旅行仪表盘', heroTitle: '欢迎回来，<br /><em>{{ user_name }}</em>', heroCopy: '从安静的山村到荒野丛林，按你想要的方式规划旅行。', startExploring: '规划新旅程', seeStory: '已保存旅程', scrollToExplore: '已保存 3 段旅程', curatedForYou: 'AI 为你推荐', exploreTitle: '探索尼泊尔<br /><em>找到你的方式。</em>', sectionIntro: '根据你的时间、体力和想带回家的故事，为你匹配路线。', dreamingOf: '我向往的地方', destinationPlaceholder: '地点或体验', travelMood: '我的旅行心情', moodAll: '任何冒险', moodMountains: '山间清风', moodCulture: '文化与宁静', moodWild: '野外探索', findMyTrip: '寻找我的旅程', heroNote: '加德满都<br /><strong>18°C · 晴</strong>', stepOne: '选择地点<br />或心情', stepTwo: '规划你的<br />完美路线', stepThree: '把旅程<br />放在一起', trustMessage: '让旅程集中在<br /><span>一个随时可用的地方。</span>', footerTagline: '深入旅行，感受更多。', saveThis: '保存这段旅程', removeSaved: '从已保存旅程中移除', emptyState: '暂时没有找到旅程。试试“山脉”“博卡拉”，或选择另一种心情。', fromLabel: '出发地', toLabel: '目的地', tripDaysLabel: '天数', departureLabel: '出发日', returnLabel: '返程日', selectCountry: '选择国家', selectPlace: '选择地点', findTrips: '寻找旅行', anyCountry: '任何国家', noTrips: '未找到合适行程', placesFound: '个目的地已为您筛选', depart: '出发', returnText: '返回' },
      ko: { label: 'KO', heroEyebrow: '나의 여행 대시보드', heroTitle: '다시 오셨네요,<br /><em>{{ user_name }}</em>', heroCopy: '조용한 산마을에서 야생 정글까지, 당신이 원하는 방식으로 여행을 설계해보세요.', startExploring: '새 여행 계획하기', seeStory: '저장한 여행', scrollToExplore: '저장한 여행 3개', curatedForYou: 'AI 추천', exploreTitle: '네팔 탐색하기<br /><em>나만의 방식으로.</em>', sectionIntro: '시간과 체력, 집으로 가져오고 싶은 이야기에 맞는 루트를 추천해드려요.', dreamingOf: '꿈꾸는 여행지', destinationPlaceholder: '장소 또는 경험', travelMood: '나의 여행 기분', moodAll: '어떤 모험이든', moodMountains: '산의 공기', moodCulture: '문화와 휴식', moodWild: '야생 속으로', findMyTrip: '내 여행 찾기', heroNote: '카트만두<br /><strong>18°C · 맑음</strong>', stepOne: '장소나 기분을<br />선택하세요', stepTwo: '나만의 완벽한<br />루트를 만드세요', stepThree: '여행을 한곳에<br />모아보세요', trustMessage: '여행을 한곳에 모아<br /><span>언제든 준비하세요.</span>', footerTagline: '더 깊이 여행하고, 더 많이 느껴보세요.', saveThis: '이 여행 저장', removeSaved: '저장한 여행에서 삭제', emptyState: '아직 여행을 찾지 못했어요. “산”, “포카라” 또는 다른 기분을 선택해 보세요.', fromLabel: '출발지', toLabel: '도착지', tripDaysLabel: '일수', departureLabel: '출발일', returnLabel: '복귀일', selectCountry: '국가 선택', selectPlace: '장소 선택', findTrips: '여행 찾기', anyCountry: '모든 국가', noTrips: '조건에 맞는 여행이 없습니다', placesFound: '개의 여행지를 찾았습니다', depart: '출발', returnText: '복귀' }
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

      const fieldLabels = {
        from: document.getElementById('from-label'),
        to: document.getElementById('to-label'),
        tripDays: document.getElementById('trip-days-label'),
        departure: document.getElementById('departure-label'),
        return: document.getElementById('return-label'),
        findTrips: document.getElementById('find-trips-button-label')
      };

      if (fieldLabels.from) fieldLabels.from.textContent = value.fromLabel;
      if (fieldLabels.to) fieldLabels.to.textContent = value.toLabel;
      if (fieldLabels.tripDays) fieldLabels.tripDays.textContent = value.tripDaysLabel;
      if (fieldLabels.departure) fieldLabels.departure.textContent = value.departureLabel;
      if (fieldLabels.return) fieldLabels.return.textContent = value.returnLabel;
      if (fieldLabels.findTrips) fieldLabels.findTrips.textContent = value.findTrips;

      const fromInput = document.getElementById('from-input');
      if (fromInput) {
        const currentFromValue = fromInput.value;
        fromInput.innerHTML = `
          <option value="">${value.selectCountry}</option>
          <option value="Japan">Japan</option>
          <option value="Korea">Korea</option>
          <option value="Australia">Australia</option>
          <option value="America">America</option>
          <option value="China">China</option>
        `;
        if (currentFromValue) fromInput.value = currentFromValue;
      }

      const toInput = document.getElementById('to-input');
      if (toInput) {
        const currentToValue = toInput.value;
        const options = [
          `<option value="">${value.selectPlace}</option>`,
          ...[...new Set(destinations.map((destination) => destination.name))].sort().map((place) => `<option value="${place}">${place}</option>`)
        ];
        toInput.innerHTML = options.join('');
        if (currentToValue) toInput.value = currentToValue;
      }

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
    const tripDaysInput = document.getElementById('trip-days');
    const departureDateInput = document.getElementById('departure-date');
    const returnDateInput = document.getElementById('return-date');
    const searchResult = document.getElementById('search-result');

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

    function renderPlaceOptions() {
      const currentToValue = toInput.value;
      const options = [
        `<option value="">${translations[currentLanguage].selectPlace}</option>`,
        ...[...new Set(destinations.map((destination) => destination.name))].sort().map((place) => `<option value="${place}">${place}</option>`)
      ];
      toInput.innerHTML = options.join('');
      if (currentToValue) toInput.value = currentToValue;
    }

    function renderDestinations() {
      const fromCountry = fromInput.value;
      const selectedPlace = toInput.value;
      const tripDays = Number.parseInt(tripDaysInput.value, 10);
      const departureDate = departureDateInput.value;
      const returnDate = returnDateInput.value;

      if (tripDays && tripDays < 3) {
        tripDaysInput.value = '3';
      }

      const effectiveTripDays = Number.isNaN(tripDays) || tripDays < 3 ? 3 : tripDays;

      const matches = destinations.filter((destination) => {
        const haystack = [destination.name, destination.region, destination.description, ...(destination.interests || []), ...(destination.best_for || [])].join(' ').toLowerCase();
        const fromMatch = !fromCountry || true;
        const toMatch = !selectedPlace || destination.name === selectedPlace || destination.region === selectedPlace;
        const tripMatch = effectiveTripDays >= 3;
        const dateMatch = !departureDate || !returnDate || new Date(returnDate) >= new Date(departureDate);

        return fromMatch && toMatch && tripMatch && dateMatch && haystack.length > 0;
      });

      if (!matches.length) {
        destinationGrid.innerHTML = '<div class="empty-state">' + translations[currentLanguage].emptyState + '</div>';
        const where = selectedPlace || 'Nepal';
        searchResult.textContent = `${translations[currentLanguage].noTrips} ${where} · ${effectiveTripDays} ${translations[currentLanguage].tripDaysLabel}`;
        return;
      }

      const fromLabel = fromCountry || translations[currentLanguage].anyCountry;
      const toLabel = selectedPlace || 'Nepal';
      const tripText = ` · ${effectiveTripDays} ${translations[currentLanguage].tripDaysLabel}`;
      const departureText = departureDate ? ` · ${translations[currentLanguage].depart} ${departureDate}` : '';
      const returnText = returnDate ? ` · ${translations[currentLanguage].returnText} ${returnDate}` : '';
      searchResult.textContent = `${matches.length} ${translations[currentLanguage].placesFound} ${fromLabel} ${translations[currentLanguage].toLabel.toLowerCase()} ${toLabel}${tripText}${departureText}${returnText}`;

      destinationGrid.innerHTML = matches.map((destination) => `
        <article class="destination-card ${destination.name === 'Kathmandu' ? 'featured-card' : ''}" data-name="${destination.name.toLowerCase()}">
          <img src="${destination.image_url || destination.image || ''}" alt="${destination.name}" />
          <div class="card-overlay"></div>
          <div class="card-content">
            <div class="card-topline"><span class="card-tag">${destination.region}</span><button class="save-button" type="button" aria-label="${translations[currentLanguage].saveThis}">♡</button></div>
            <h3>${destination.name}</h3>
            <div class="card-meta"><span>⌁ ${destination.daily_cost ? '$' + destination.daily_cost + '/day' : 'Flexible'}</span><span>↗ ${destination.best_for ? destination.best_for.join(', ') : 'Adventure'}</span></div>
          </div>
        </article>
      `).join('');
    }

    document.getElementById('dashboard-search').addEventListener('submit', (event) => {
      event.preventDefault();
      renderDestinations();
    });

    fromInput.addEventListener('change', renderDestinations);
    toInput.addEventListener('change', renderDestinations);
    tripDaysInput.addEventListener('input', renderDestinations);
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

    renderPlaceOptions();
    updateTexts(currentLanguage);
    syncDateConstraints();
    renderDestinations();
  </script>
</body>
</html>
"""

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #f4fbff, #e8f7ef);
      margin: 0;
      padding: 40px;
      color: #1d2a3a;
    }
    .topbar {
      max-width: 1200px;
      margin: 0 auto 16px auto;
      display: flex;
      justify-content: flex-end;
    }
    .language-box {
      display: flex;
      align-items: center;
      gap: 10px;
      background: white;
      padding: 10px 14px;
      border-radius: 12px;
      box-shadow: 0 8px 20px rgba(15, 118, 110, 0.08);
      border: 1px solid #e2e8f0;
    }
    .container {
      max-width: 1200px;
      margin: auto;
      background: white;
      padding: 30px;
      border-radius: 18px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    }
    h1 {
      text-align: center;
      color: #0f766e;
    }
    form {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
      margin-top: 25px;
    }
    .field {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    label {
      font-weight: bold;
    }
    input, select, button {
      padding: 12px 14px;
      border-radius: 10px;
      border: 1px solid #cbd5e1;
      font-size: 16px;
    }
    button {
      background: #0f766e;
      color: white;
      border: none;
      cursor: pointer;
      font-weight: bold;
    }
    .flow {
      margin-top: 25px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .step {
      background: #dff7f0;
      color: #14532d;
      padding: 8px 12px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: bold;
    }
    .map-layout {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 20px;
      margin-top: 25px;
    }
    .map-panel, .side-panel {
      background: #f8fafc;
      border-radius: 14px;
      padding: 16px;
      border: 1px solid #e2e8f0;
    }
    #map {
      height: 440px;
      width: 100%;
      border-radius: 12px;
    }
    .details-box {
      background: white;
      padding: 16px;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
    }
    .results {
      margin-top: 30px;
      padding: 20px;
      background: #f8fafc;
      border-radius: 12px;
    }
    .card {
      margin-top: 18px;
      padding: 18px;
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 10px 24px rgba(15, 118, 110, 0.08);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
      transform: translateY(-2px);
      box-shadow: 0 14px 28px rgba(15, 118, 110, 0.12);
    }
    .destination-image {
      width: 100%;
      height: 240px;
      object-fit: cover;
      border-radius: 14px;
      margin-bottom: 16px;
      display: block;
      border: 2px solid rgba(15, 118, 110, 0.08);
      box-shadow: 0 10px 20px rgba(15, 23, 42, 0.12);
    }
    @media (max-width: 900px) {
      .map-layout {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="topbar">
    <div class="language-box">
      <label>{{ language }}</label>
      <select id="language-select" onchange="const lang=this.value; const target = window.location.pathname === '/plan' ? '/' : window.location.pathname; const url = new URL(target, window.location.origin); url.searchParams.set('lang', lang); window.location.href = url.toString();">
        <option value="en" {% if selected_language == 'en' %}selected{% endif %}>English</option>
        <option value="ja" {% if selected_language == 'ja' %}selected{% endif %}>日本語</option>
        <option value="zh" {% if selected_language == 'zh' %}selected{% endif %}>中文</option>
        <option value="ko" {% if selected_language == 'ko' %}selected{% endif %}>한국어</option>
      </select>
    </div>
  </div>

  <div class="container">
    <h1>{{ title }}</h1>
    <p style="text-align:center; color:#475569;">{{ subtitle }}</p>

    <form method="post" action="/plan?lang={{ selected_language }}">
      <input type="hidden" name="language" value="{{ selected_language }}">

      <div style="grid-column: 1 / -1; margin-bottom: 6px; color: #475569; font-size: 14px;">
        Choose a region or season to narrow down the best places for your trip.
      </div>

      <div class="field">
        <label>{{ trip_days }}</label>
        <small>3–30 days</small>
        <input type="number" name="days" value="3" min="3" max="30" required>
      </div>

      <div class="field">
        <label>{{ budget }}</label>
        <small>NPR 150,000 – 1,000,000</small>
        <input type="number" name="budget" value="150000" min="150000" max="1000000" step="5000" required>
      </div>

      <div class="field">
        <label>{{ region }}</label>
        <select name="region">
          <option value="" selected>Select</option>
          <option value="Eastern">{{ region_eastern }}</option>
          <option value="Central">{{ region_central }}</option>
          <option value="Western">{{ region_western }}</option>
          <option value="Northern">{{ region_northern }}</option>
          <option value="Southern">{{ region_southern }}</option>
        </select>
      </div>

      <div class="field">
        <label>{{ interests }}</label>
        <input type="text" name="interests" value="" placeholder="Type interests like culture, trekking, food">
      </div>

      <div class="field">
        <label>{{ season }}</label>
        <select name="season">
          <option value="" selected>Select</option>
          <option value="spring">{{ season_spring }}</option>
          <option value="summer">{{ season_summer }}</option>
          <option value="autumn">{{ season_autumn }}</option>
          <option value="winter">{{ season_winter }}</option>
        </select>
      </div>

      <div class="field" style="justify-content:end;">
        <button type="submit">{{ generate }}</button>
      </div>
    </form>

    <div class="map-layout">
      <div class="map-panel">
        <h2>{{ map_view }}</h2>
        <div id="map"></div>
      </div>
      <div class="side-panel">
        <h2>{{ details }}</h2>
        <div id="selected-details" class="details-box">
          <p>{{ select_marker }}</p>
        </div>
      </div>
    </div>

    {% if result %}
    <div class="results">
      <h2>{{ trip_suggestions }}</h2>
      <p>{{ result.message }}</p>
      <p><strong>{{ total }}:</strong> ${{ result.estimated_total }}</p>

      {% for item in result.recommendations %}
      <div class="card">
        {% set image_src = item.image if item.image is defined else item.image_url %}
        <img class="destination-image" src="{{ image_src }}" alt="{{ item.name }}" />
        <h3>{{ item.name }}</h3>
        <p><strong>Region:</strong> {{ item.region }}</p>
        <p><strong>{{ daily_cost }}:</strong> ${{ item.daily_cost }}</p>
        <p><strong>{{ total }}:</strong> ${{ item.estimated_total }}</p>
        <p><strong>Interests:</strong> {{ ', '.join(item.interests) }}</p>
        <p><strong>{{ best_for }}:</strong> {{ ', '.join(item.best_for) }}</p>
        <p>{{ item.description }}</p>
      </div>
      {% endfor %}
    </div>
    {% endif %}
  </div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const destinations = {{ (result.recommendations if result else [])|tojson|safe }};
    const map = L.map('map').setView([28.3949, 84.1240], 7);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const allPlaces = {
      Kathmandu: [27.7172, 85.3240],
      Pokhara: [28.2096, 83.9856],
      Chitwan: [27.5291, 84.3542],
      Lumibini: [27.4876, 83.2743],
      Mustang: [29.1980, 83.9282],
      Nagarkot: [27.7127, 85.5231],
      'Everest Base Camp Region': [27.9881, 86.9250],
      Bhaktapur: [27.6729, 85.4279]
    };

    const points = destinations.map(item => {
      const latlng = allPlaces[item.name] || [28.3949, 84.1240];
      return { ...item, lat: latlng[0], lng: latlng[1] };
    });

    const routeLine = points.length > 1 ? L.polyline(
      points.map(p => [p.lat, p.lng]),
      { color: '#0f766e', weight: 4, opacity: 0.8 }
    ).addTo(map) : null;

    if (routeLine) {
      map.fitBounds(routeLine.getBounds(), { padding: [30, 30] });
    } else if (points.length === 1) {
      map.setView([points[0].lat, points[0].lng], 9);
    }

    const detailsBox = document.getElementById('selected-details');

    function renderDetails(item) {
      detailsBox.innerHTML = `
        <h3>${item.name}</h3>
        <p><strong>Region:</strong> ${item.region}</p>
        <p><strong>Estimated total:</strong> $${item.estimated_total}</p>
        <p><strong>Daily cost:</strong> $${item.daily_cost}</p>
        <p><strong>Best for:</strong> ${item.best_for.join(', ')}</p>
        <p><strong>Interests:</strong> ${item.interests.join(', ')}</p>
        <p>${item.description}</p>
      `;
    }

    points.forEach((item) => {
      const marker = L.marker([item.lat, item.lng]).addTo(map);
      marker.bindPopup(`<strong>${item.name}</strong><br>${item.description}`);
      marker.on('click', () => renderDetails(item));
    });

    if (points.length > 0) {
      renderDetails(points[0]);
    }
  </script>
</body>
</html>
"""


@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, "images"), filename)


@app.route("/signup.html")
def signup_page():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return send_from_directory(project_root, "signup.html")


@app.route("/signin.html")
def signin_page():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return send_from_directory(project_root, "signin.html")


@app.route("/index.html")
def index_page():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return send_from_directory(project_root, "index.html")


@app.route("/styles.css")
def styles_page():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return send_from_directory(project_root, "styles.css")


@app.route("/<path:filename>")
def serve_project_file(filename):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return send_from_directory(project_root, filename)


@app.route("/", methods=["GET", "POST"])
def home():
    selected_language = request.args.get("lang") or request.form.get("language") or "en"
    texts = get_translation(selected_language)
    return render_template_string(HTML, result=None, selected_language=selected_language, **texts)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/signin.html")
    return render_template_string(
        DASHBOARD_HTML,
        user_name=session.get("user_name", "Traveler"),
        destinations=DESTINATIONS,
    )


@app.route("/plan", methods=["GET", "POST"])
def plan_trip():
    selected_language = request.args.get("lang") or request.form.get("language") or "en"
    texts = get_translation(selected_language)

    if request.method == "GET":
        return render_template_string(HTML, result=None, selected_language=selected_language, **texts)

    days = int(request.form.get("days", 0) or 0)
    budget = int(request.form.get("budget", 0) or 0)

    region = (request.form.get("region") or "").strip()
    if region.lower() in {"select", "", "all", "any"}:
        region = ""

    interests = [item.strip().lower() for item in request.form.get("interests", "").split(",") if item.strip()]

    season = (request.form.get("season") or "").strip()
    if season.lower() in {"select", "", "all", "any"}:
        season = ""
    else:
        season = season.lower()

    if not region and not season:
        return render_template_string(
            HTML,
            result={
                "recommendations": [],
                "estimated_total": 0,
                "message": "Please select a region or season to see matching places.",
            },
            selected_language=selected_language,
            **texts,
        )

    result = planner.generate_itinerary(
        days=days,
        budget_usd=budget,
        region=region,
        interests=interests,
        season=season,
    )

    return render_template_string(HTML, result=result, selected_language=selected_language, **texts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
