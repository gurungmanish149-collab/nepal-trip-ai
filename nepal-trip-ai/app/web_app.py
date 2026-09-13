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
    .search-result { max-width: 1300px; margin: 0 auto 13px; }
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
      en: { label: 'EN', heroEyebrow: 'Your trip dashboard', heroTitle: 'Welcome back,<br /><em>{{ user_name }}</em>', heroCopy: 'From quiet mountain villages to wild jungle trails, discover a journey shaped around the way you want to travel.', startExploring: 'Plan a new trip', seeStory: 'Saved trips', scrollToExplore: '3 saved trips', curatedForYou: 'AI recommendations', exploreTitle: 'Explore Nepal<br /><em>your way.</em>', sectionIntro: 'Routes matched to your time, energy, and the kind of stories you want to bring home.', dreamingOf: "I'm dreaming of", destinationPlaceholder: 'A place or experience', travelMood: 'My travel mood', moodAll: 'Any kind of adventure', moodMountains: 'Mountain air', moodCulture: 'Culture & calm', moodWild: 'Wild escapes', findMyTrip: 'Find my trip', heroNote: 'Kathmandu<br /><strong>18°C · Clear</strong>', stepOne: 'Pick a place<br />or feeling', stepTwo: 'Shape your<br />perfect route', stepThree: 'Keep it<br />all together', trustMessage: 'Your trip, in one place<br /><span>ready when you are.</span>', footerTagline: 'Travel deeper. Feel more.', saveThis: 'Save this trip', removeSaved: 'Remove from saved trips', emptyState: 'No journeys found yet. Try “mountain”, “Pokhara”, or choose another mood.', fromLabel: 'From', toLabel: 'To', departureLabel: 'Departure', returnLabel: 'Return', selectCountry: 'Select country', selectPlace: 'Select place', findTrips: 'Search', anyCountry: 'Any country', noTrips: 'No trips found for', placesFound: 'places found from', depart: 'Depart', returnText: 'Return', daysLabel: 'days', totalLabel: 'Total', flightLabel: 'Flight', tripCostLabel: 'trip costs' },
      ja: { label: 'JA', heroEyebrow: 'あなたの旅ダッシュボード', heroTitle: 'お帰りなさい、<br /><em>{{ user_name }}</em>', heroCopy: '静かな山村から野生のジャングルまで、あなたらしい旅を形にしましょう。', startExploring: '新しい旅を計画', seeStory: '保存した旅', scrollToExplore: '保存した旅 3件', curatedForYou: 'AIおすすめ', exploreTitle: 'ネパールを探す<br /><em>あなたらしく。</em>', sectionIntro: '時間、体力、持ち帰りたい物語に合わせたルートをご提案します。', dreamingOf: '夢見ている場所', destinationPlaceholder: '場所や体験を入力', travelMood: '旅の気分', moodAll: 'すべての冒険', moodMountains: '山の空気', moodCulture: '文化と癒やし', moodWild: '野生の旅', findMyTrip: '旅を見つける', heroNote: 'カトマンズ<br /><strong>18°C · 晴れ</strong>', stepOne: '場所や気分を<br />選ぶ', stepTwo: 'ぴったりのルートを<br />つくる', stepThree: '旅をひとつに<br />まとめる', trustMessage: '旅をひとつの場所に<br /><span>いつでも準備万端。</span>', footerTagline: '深く旅して、もっと感じる。', saveThis: 'この旅を保存', removeSaved: '保存済みから削除', emptyState: '旅が見つかりません。「山」「ポカラ」または別の気分を試してください。', fromLabel: '出発地', toLabel: '目的地', departureLabel: '出発日', returnLabel: '帰国日', selectCountry: '国を選択', selectPlace: '場所を選択', findTrips: '検索', anyCountry: 'どの国でも', noTrips: '該当の旅程が見つかりません', placesFound: '件の候補が見つかりました', depart: '出発', returnText: '帰着', daysLabel: '日', totalLabel: '合計', flightLabel: '航空券', tripCostLabel: '旅行費用' },
      zh: { label: 'ZH', heroEyebrow: '你的旅行仪表盘', heroTitle: '欢迎回来，<br /><em>{{ user_name }}</em>', heroCopy: '从安静的山村到荒野丛林，按你想要的方式规划旅行。', startExploring: '规划新旅程', seeStory: '已保存旅程', scrollToExplore: '已保存 3 段旅程', curatedForYou: 'AI 为你推荐', exploreTitle: '探索尼泊尔<br /><em>找到你的方式。</em>', sectionIntro: '根据你的时间、体力和想带回家的故事，为你匹配路线。', dreamingOf: '我向往的地方', destinationPlaceholder: '地点或体验', travelMood: '我的旅行心情', moodAll: '任何冒险', moodMountains: '山间清风', moodCulture: '文化与宁静', moodWild: '野外探索', findMyTrip: '寻找我的旅程', heroNote: '加德满都<br /><strong>18°C · 晴</strong>', stepOne: '选择地点<br />或心情', stepTwo: '规划你的<br />完美路线', stepThree: '把旅程<br />放在一起', trustMessage: '让旅程集中在<br /><span>一个随时可用的地方。</span>', footerTagline: '深入旅行，感受更多。', saveThis: '保存这段旅程', removeSaved: '从已保存旅程中移除', emptyState: '暂时没有找到旅程。试试“山脉”“博卡拉”，或选择另一种心情。', fromLabel: '出发地', toLabel: '目的地', departureLabel: '出发日', returnLabel: '返程日', selectCountry: '选择国家', selectPlace: '选择地点', findTrips: '搜索', anyCountry: '任何国家', noTrips: '未找到合适行程', placesFound: '个目的地已为您筛选', depart: '出发', returnText: '返回', daysLabel: '天', totalLabel: '总价', flightLabel: '机票', tripCostLabel: '旅行费用' },
      ko: { label: 'KO', heroEyebrow: '나의 여행 대시보드', heroTitle: '다시 오셨네요,<br /><em>{{ user_name }}</em>', heroCopy: '조용한 산마을에서 야생 정글까지, 당신이 원하는 방식으로 여행을 설계해보세요.', startExploring: '새 여행 계획하기', seeStory: '저장한 여행', scrollToExplore: '저장한 여행 3개', curatedForYou: 'AI 추천', exploreTitle: '네팔 탐색하기<br /><em>나만의 방식으로.</em>', sectionIntro: '시간과 체력, 집으로 가져오고 싶은 이야기에 맞는 루트를 추천해드려요.', dreamingOf: '꿈꾸는 여행지', destinationPlaceholder: '장소 또는 경험', travelMood: '나의 여행 기분', moodAll: '어떤 모험이든', moodMountains: '산의 공기', moodCulture: '문화와 휴식', moodWild: '야생 속으로', findMyTrip: '내 여행 찾기', heroNote: '카트만두<br /><strong>18°C · 맑음</strong>', stepOne: '장소나 기분을<br />선택하세요', stepTwo: '나만의 완벽한<br />루트를 만드세요', stepThree: '여행을 한곳에<br />모아보세요', trustMessage: '여행을 한곳에 모아<br /><span>언제든 준비하세요.</span>', footerTagline: '더 깊이 여행하고, 더 많이 느껴보세요.', saveThis: '이 여행 저장', removeSaved: '저장한 여행에서 삭제', emptyState: '아직 여행을 찾지 못했어요. “산”, “포카라” 또는 다른 기분을 선택해 보세요.', fromLabel: '출발지', toLabel: '도착지', departureLabel: '출발일', returnLabel: '복귀일', selectCountry: '국가 선택', selectPlace: '장소 선택', findTrips: '검색', anyCountry: '모든 국가', noTrips: '조건에 맞는 여행이 없습니다', placesFound: '개의 여행지를 찾았습니다', depart: '출발', returnText: '복귀', daysLabel: '일', totalLabel: '총액', flightLabel: '항공권', tripCostLabel: '여행 경비' }
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

    function renderPlaceOptions() {
      const currentToValue = toInput.value;
      const options = [
        `<option value="">${translations[currentLanguage].selectPlace}</option>`,
        ...[...new Set(destinations.map((destination) => destination.name))].sort().map((place) => `<option value="${place}">${place}</option>`)
      ];
      toInput.innerHTML = options.join('');
      if (currentToValue) toInput.value = currentToValue;
    }

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

    function renderDestinations(options = {}) {
      const { openPopup = false } = options;
      const fromCountry = fromInput.value;
      const selectedPlace = toInput.value;
      const departureDate = departureDateInput.value;
      const returnDate = returnDateInput.value;

      const matches = destinations.filter((destination) => {
        const haystack = [destination.name, destination.region, destination.description, ...(destination.interests || []), ...(destination.best_for || [])].join(' ').toLowerCase();
        const fromMatch = !fromCountry || true;
        const toMatch = !selectedPlace || destination.name === selectedPlace || destination.region === selectedPlace;
        const dateMatch = !departureDate || !returnDate || new Date(returnDate) >= new Date(departureDate);

        return fromMatch && toMatch && dateMatch && haystack.length > 0;
      });

      destinationGrid.innerHTML = '';
      destinationGrid.style.display = 'none';

      if (!matches.length) {
        closeDestinationModal();
        const where = selectedPlace || 'Nepal';
        searchResult.textContent = `${translations[currentLanguage].noTrips} ${where}`;
        return;
      }

      const fromLabel = fromCountry || translations[currentLanguage].anyCountry;
      const toLabel = selectedPlace || 'Nepal';
      const departureText = departureDate ? ` · ${translations[currentLanguage].depart} ${departureDate}` : '';
      const returnText = returnDate ? ` · ${translations[currentLanguage].returnText} ${returnDate}` : '';
      const selectedDestination = selectedPlace ? (matches.find((destination) => destination.name === selectedPlace) || matches[0]) : matches[0];
      const tripCost = getTripCostEstimate(selectedDestination, fromCountry || 'Japan', departureDate || '2026-09-14', returnDate || '2026-09-19');
      const lang = translations[currentLanguage];

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

      destinationGrid.innerHTML = '';
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
<html lang="ja">
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
