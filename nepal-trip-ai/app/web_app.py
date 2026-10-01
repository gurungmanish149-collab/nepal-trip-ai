from datetime import date, timedelta
from pathlib import Path

from flask import Blueprint, redirect, render_template_string, request, send_from_directory, session

from .planner import TravelPlanner


planner_pages = Blueprint("planner_pages", __name__)
planner = TravelPlanner()
COUNTRIES = ("Japan", "America", "Australia", "China", "Korea", "Mongolia", "UK")
NEPAL_PLACES = (
  {"name": "Everest Base Camp", "image": "/images/langtang4.jpg"},
  {"name": "Pokhara Lakeside", "image": "/images/manaslu.jpg"},
  {"name": "Chitwan Wild", "image": "/images/sun-koshi-river-rafting-nepal.webp"},
  {"name": "Annapurna Region", "image": "/images/manaslu.jpg"},
  {"name": "Mustang", "image": "/images/langtang4.jpg"},
  {"name": "Ilam", "image": "/images/ilam.jpg"},
  {"name": "Janakpur", "image": "/images/patan.jpg"},
  {"name": "Bardiya", "image": "/images/sun-koshi-river-rafting-nepal.webp"},
  {"name": "Bandipur", "image": "/images/bandipur.jpg"},
  {"name": "Bhaktapur", "image": "/images/bhaktapur.jpg"},
  {"name": "Patan (Lalitpur)", "image": "/images/patan.jpg"},
  {"name": "Nagarkot", "image": "/images/langtang4.jpg"},
  {"name": "Langtang Region", "image": "/images/langtang4.jpg"},
  {"name": "Palpa / Tansen", "image": "/images/palpa.jpg"},
  {"name": "Manaslu Region", "image": "/images/manaslu.jpg"},
  {"name": "Rara Lake", "image": "/images/sun-koshi-river-rafting-nepal.webp"},
  {"name": "Koshi Tappu", "image": "/images/sun-koshi-river-rafting-nepal.webp"},
  {"name": "Kanchenjunga Region", "image": "/images/manaslu.jpg"},
)
PLACE_ALIASES = {
    "Everest Base Camp": "Everest Base Camp Region",
    "Pokhara Lakeside": "Pokhara",
    "Chitwan Wild": "Chitwan",
  }
EXTRA_PLACE_DETAILS = {
    "Annapurna Region": ("Northern", 100, 28.5960, 83.8200, "Mountains and trekking across a classic Himalayan route.", ["trekking", "mountains"], ["scenic_views", "adventure"]),
    "Ilam": ("Eastern", 60, 26.9094, 88.0175, "Tea gardens, green hills, and peaceful nature.", ["nature", "tea", "culture"], ["slow_travel", "scenic_views"]),
    "Janakpur": ("Southern", 55, 26.7288, 85.9263, "Temples and Mithila culture in a historic pilgrimage city.", ["culture", "history", "religion"], ["heritage", "photography"]),
    "Bardiya": ("Western", 80, 28.3889, 81.3150, "Wildlife, river forests, and quiet nature in western Nepal.", ["wildlife", "nature"], ["wildlife", "adventure"]),
    "Bandipur": ("Western", 60, 27.9380, 84.4060, "A traditional hill town with wide Himalayan views.", ["culture", "mountains"], ["heritage", "scenic_views"]),
    "Patan (Lalitpur)": ("Central", 60, 27.6640, 85.3188, "Temples, fine arts, and Newari craft traditions.", ["culture", "heritage", "art"], ["history", "photography"]),
    "Langtang Region": ("Northern", 95, 28.2117, 85.5612, "Mountain trails, glaciers, and Tamang villages.", ["trekking", "mountains", "nature"], ["adventure", "scenic_views"]),
    "Palpa / Tansen": ("Western", 55, 27.8670, 83.5460, "Hilltop history, local culture, and winding old streets.", ["culture", "history"], ["heritage", "slow_travel"]),
    "Manaslu Region": ("Western", 100, 28.5497, 84.5597, "Remote Himalayan trekking and dramatic high mountain scenery.", ["trekking", "mountains", "nature"], ["adventure", "remote_trip"]),
    "Rara Lake": ("Western", 90, 29.5300, 82.0800, "A remote mountain lake surrounded by forest and quiet trails.", ["nature", "lake", "wildlife"], ["scenic_views", "remote_trip"]),
    "Koshi Tappu": ("Eastern", 70, 26.6667, 87.0000, "Wetlands, migratory birds, and rich wildlife.", ["wildlife", "nature", "birding"], ["wildlife", "photography"]),
    "Kanchenjunga Region": ("Eastern", 110, 27.7025, 88.1475, "Remote trails beneath Nepal's far-eastern Himalayan peaks.", ["trekking", "mountains", "nature"], ["adventure", "remote_trip"]),
}
COUNTRY_AIRFARE_ESTIMATES_USD = {
    "Japan": 650,
    "America": 1200,
    "Australia": 1100,
    "China": 550,
    "Korea": 650,
    "Mongolia": 750,
    "UK": 1050,
}
DESTINATION_FLIGHT_ESTIMATES_USD = {
    "Pokhara": 200,
    "Pokhara Lakeside": 200,
    "Chitwan": 120,
    "Chitwan Wild": 120,
    "Lumbini": 100,
    "Mustang": 250,
    "Everest Base Camp Region": 250,
    "Everest Base Camp": 250,
    "Rara Lake": 250,
    "Langtang Region": 180,
    "Manaslu Region": 180,
    "Kanchenjunga Region": 250,
}
DESTINATION_DETAIL_TRANSLATIONS = {
    "ja": {
        "Pokhara": {
            "region": "西部",
            "description": "山々の景色を眺め、湖畔を散策し、さまざまなアクティビティを楽しめます。",
            "best_for": ["絶景", "冒険"],
            "interests": ["自然", "トレッキング", "湖", "リラックス"],
        },
    },
    "zh": {
        "Pokhara": {
            "region": "西部",
            "description": "欣赏群山景色、漫步湖畔，并体验丰富的户外活动。",
            "best_for": ["风景", "冒险"],
            "interests": ["自然", "徒步", "湖泊", "休闲"],
        },
    },
    "ko": {
        "Pokhara": {
            "region": "서부",
            "description": "산 전망을 감상하고 호숫가를 산책하며 다양한 야외 활동을 즐길 수 있습니다.",
            "best_for": ["풍경", "모험"],
            "interests": ["자연", "트레킹", "호수", "휴식"],
        },
    },
}
for localized_destinations in DESTINATION_DETAIL_TRANSLATIONS.values():
    localized_destinations["Pokhara Lakeside"] = localized_destinations["Pokhara"]


def build_destination_catalog():
    destinations_by_name = {destination["name"]: dict(destination) for destination in planner.destinations}
    catalog = list(destinations_by_name.values())
    for place in NEPAL_PLACES:
        if place["name"] in destinations_by_name:
            continue
        source_name = PLACE_ALIASES.get(place["name"])
        if source_name:
            destination = dict(destinations_by_name[source_name])
            destination["name"] = place["name"]
            destination["image_url"] = place["image"]
        else:
            region, daily_cost, lat, lng, description, interests, best_for = EXTRA_PLACE_DETAILS[place["name"]]
            destination = {
                "name": place["name"],
                "region": region,
                "daily_cost": daily_cost,
                "lat": lat,
                "lng": lng,
                "description": description,
                "interests": interests,
                "best_for": best_for,
                "season": ["spring", "autumn"],
                "image_url": place["image"],
            }
        catalog.append(destination)
    return catalog


DESTINATION_CATALOG = build_destination_catalog()
planner.destinations = DESTINATION_CATALOG

TRANSLATIONS = {
    "en": {
        "title": "NepalTrip AI",
        "subtitle": "Smart Nepal Travel Planner",
        "country": "Country",
        "destination": "Destination",
        "depart_date": "Departure date",
        "return_date": "Return date",
        "season": "Season",
        "generate": "Generate Itinerary",
        "search": "Search",
        "nav_explore": "Explore",
        "nav_trips": "My trips",
        "nav_recommendations": "Recommendations",
        "sign_out": "Sign out",
        "hero_copy": "Choose your pace, dates, and a destination for your Nepal trip.",
        "hero_note": "Nepal",
        "hero_note_subtitle": "Destinations · Itineraries",
        "footer_explore": "Back to explore",
        "results_found": "Destination matched your trip.",
        "no_matches": "No destinations match these travel dates.",
        "planner_intro": "Choose your country, destination, and travel dates.",
        "country_placeholder": "Select country",
        "destination_placeholder": "Select destination",
        "any_season": "Any season",
        "places_eyebrow": "Explore Nepal",
        "places_title": "Places to discover.",
        "dialog_country": "Country",
        "dialog_destination": "Destination",
        "dialog_region": "Region",
        "dialog_trip_cost": "Estimated trip cost",
        "dialog_daily_cost": "Daily cost",
        "dialog_flight_cost": "Estimated round-trip airfare",
        "dialog_total": "Estimated total with airfare",
        "dialog_best_for": "Best for",
        "dialog_interests": "Interests",
        "dialog_close": "Close",
        "dialog_estimate_note": "Airfare is an approximate planning estimate, not a live ticket quote.",
        "dialog_dates_note": "Choose travel dates to calculate the trip total.",
        "error_past_date": "Departure date cannot be in the past.",
        "error_invalid_date": "Please enter valid travel dates.",
        "error_country": "Please choose a country.",
        "error_destination": "Please choose a Nepal destination.",
        "details": "Destination Details",
        "select": "Select",
        "placeholder": "Culture / Food / Trekking / Nature / Adventure / History",
        "flight": "Travel Preferences",
        "backend": "Python Backend",
        "database": "Destination Database",
        "route": "Trip details",
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
        "country": "出発国",
        "destination": "目的地",
        "depart_date": "出発日",
        "return_date": "帰着日",
        "season": "季節",
        "generate": "旅程を生成",
        "search": "検索",
        "nav_explore": "探索",
        "nav_trips": "旅行プラン",
        "nav_recommendations": "おすすめ",
        "sign_out": "ログアウト",
        "hero_copy": "日程と目的地を選んで、ネパール旅行を計画しましょう。",
        "hero_note": "ネパール",
        "hero_note_subtitle": "目的地 · 旅程",
        "footer_explore": "探索に戻る",
        "results_found": "ご希望に合う目的地が見つかりました。",
        "no_matches": "旅行日程に合う目的地が見つかりません。",
        "planner_intro": "出発国、目的地、旅行日程を選択してください。",
        "country_placeholder": "国を選択",
        "destination_placeholder": "目的地を選択",
        "any_season": "すべての季節",
        "places_eyebrow": "ネパールを探す",
        "places_title": "訪れたい場所。",
        "dialog_country": "出発国",
        "dialog_destination": "目的地",
        "dialog_region": "地域",
        "dialog_trip_cost": "旅行費用の目安",
        "dialog_daily_cost": "1日あたりの費用",
        "dialog_flight_cost": "往復航空券の概算",
        "dialog_total": "航空券込みの合計目安",
        "dialog_best_for": "おすすめ",
        "dialog_interests": "楽しみ方",
        "dialog_close": "閉じる",
        "dialog_estimate_note": "航空運賃は計画用の概算です。リアルタイムの航空券価格ではありません。",
        "dialog_dates_note": "旅行日を選択すると旅行費用を計算できます。",
        "error_past_date": "出発日に過去の日付は選択できません。",
        "error_invalid_date": "有効な旅行日を入力してください。",
        "error_country": "出発国を選択してください。",
        "error_destination": "ネパールの目的地を選択してください。",
        "details": "観光地の詳細",
        "select": "選択",
        "placeholder": "文化, トレッキング, 自然",
        "flight": "旅行の好み",
        "backend": "Pythonバックエンド",
        "database": "観光地データベース",
        "route": "旅行の詳細",
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
        "country": "出发国家",
        "destination": "目的地",
        "depart_date": "出发日期",
        "return_date": "返程日期",
        "season": "季节",
        "generate": "生成行程",
        "search": "搜索",
        "nav_explore": "探索",
        "nav_trips": "我的行程",
        "nav_recommendations": "推荐",
        "sign_out": "退出登录",
        "hero_copy": "选择日期和目的地，规划你的尼泊尔之旅。",
        "hero_note": "尼泊尔",
        "hero_note_subtitle": "目的地 · 行程",
        "footer_explore": "返回探索",
        "results_found": "找到符合行程的目的地。",
        "no_matches": "没有符合旅行日期的目的地。",
        "planner_intro": "选择出发国家、目的地和旅行日期。",
        "country_placeholder": "选择国家",
        "destination_placeholder": "选择目的地",
        "any_season": "任何季节",
        "places_eyebrow": "探索尼泊尔",
        "places_title": "值得发现的地方。",
        "dialog_country": "出发国家",
        "dialog_destination": "目的地",
        "dialog_region": "地区",
        "dialog_trip_cost": "预计旅行费用",
        "dialog_daily_cost": "每日费用",
        "dialog_flight_cost": "往返机票估算",
        "dialog_total": "含机票预计总额",
        "dialog_best_for": "适合",
        "dialog_interests": "兴趣",
        "dialog_close": "关闭",
        "dialog_estimate_note": "机票仅为规划估算，并非实时票价。",
        "dialog_dates_note": "选择旅行日期以计算总费用。",
        "error_past_date": "出发日期不能早于今天。",
        "error_invalid_date": "请输入有效的旅行日期。",
        "error_country": "请选择出发国家。",
        "error_destination": "请选择尼泊尔目的地。",
        "details": "目的地详情",
        "select": "选择",
        "placeholder": "文化, 徒步, 自然",
        "flight": "旅行偏好",
        "backend": "Python后端",
        "database": "目的地数据库",
        "route": "行程详情",
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
        "country": "출발 국가",
        "destination": "여행지",
        "depart_date": "출발일",
        "return_date": "귀국일",
        "season": "시즌",
        "generate": "여행 코스 생성",
        "search": "검색",
        "nav_explore": "둘러보기",
        "nav_trips": "내 여행",
        "nav_recommendations": "추천 여행지",
        "sign_out": "로그아웃",
        "hero_copy": "여행 날짜와 목적지를 선택해 네팔 여행을 계획하세요.",
        "hero_note": "네팔",
        "hero_note_subtitle": "여행지 · 일정",
        "footer_explore": "둘러보기로 돌아가기",
        "results_found": "여행 조건에 맞는 여행지를 찾았습니다.",
        "no_matches": "여행 날짜에 맞는 여행지가 없습니다.",
        "planner_intro": "출발 국가, 여행지와 여행 날짜를 선택하세요.",
        "country_placeholder": "국가 선택",
        "destination_placeholder": "여행지 선택",
        "any_season": "모든 시즌",
        "places_eyebrow": "네팔 둘러보기",
        "places_title": "발견할 여행지.",
        "dialog_country": "출발 국가",
        "dialog_destination": "여행지",
        "dialog_region": "지역",
        "dialog_trip_cost": "예상 여행 비용",
        "dialog_daily_cost": "일일 비용",
        "dialog_flight_cost": "왕복 항공권 예상 비용",
        "dialog_total": "항공권 포함 예상 합계",
        "dialog_best_for": "추천 대상",
        "dialog_interests": "관심사",
        "dialog_close": "닫기",
        "dialog_estimate_note": "항공권은 계획용 예상 금액이며 실시간 가격이 아닙니다.",
        "dialog_dates_note": "여행 비용을 계산하려면 여행 날짜를 선택하세요.",
        "error_past_date": "출발일은 오늘 이전으로 선택할 수 없습니다.",
        "error_invalid_date": "유효한 여행 날짜를 입력하세요.",
        "error_country": "출발 국가를 선택하세요.",
        "error_destination": "네팔 여행지를 선택하세요.",
        "details": "여행지 정보",
        "select": "선택",
        "placeholder": "문화, 트레킹, 자연",
        "flight": "여행 선호도",
        "backend": "Python 백엔드",
        "database": "여행지 데이터베이스",
        "route": "여행 정보",
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


HTML = """
<!doctype html>
<html lang="{{ selected_language }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} | Himalaya</title>
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
  <link rel="stylesheet" href="/styles.css">
</head>
<body class="planner-page">
  <header class="site-header">
    <a class="brand" href="/" aria-label="Himalaya home">
      <span class="brand-mark">G</span>
      <span>himalaya<span class="brand-dot">.</span></span>
    </a>
    <nav class="main-nav" id="planner-nav" aria-label="Main navigation">
      <a href="/#explore">{{ nav_explore }}</a>
      <a class="active" href="#planner">{{ nav_trips }}</a>
      <a href="#results">{{ nav_recommendations }}</a>
    </nav>
    <div class="header-actions">
      <span class="planner-user">{{ user_name }}</span>
      <label class="planner-language-picker">
        <span class="visually-hidden">{{ language }}</span>
      <select id="language-select" onchange="changeDashboardLanguage(this.value)">
        <option value="en" {% if selected_language == 'en' %}selected{% endif %}>English</option>
        <option value="ja" {% if selected_language == 'ja' %}selected{% endif %}>日本語</option>
        <option value="zh" {% if selected_language == 'zh' %}selected{% endif %}>中文</option>
        <option value="ko" {% if selected_language == 'ko' %}selected{% endif %}>한국어</option>
      </select>
      </label>
      <form class="planner-logout" method="post" action="/dashboard/signout">
        <button class="sign-in" type="submit">{{ sign_out }}</button>
      </form>
      <button class="menu-toggle" id="planner-menu-toggle" type="button" aria-label="Open menu" aria-expanded="false">☰</button>
    </div>
  </header>

  <main id="top">
    <section class="hero app-dashboard planner-hero" aria-labelledby="planner-title">
      <div class="hero-content">
        <p class="eyebrow"><span class="eyebrow-line"></span>{{ flight }}</p>
        <h1 id="planner-title">{{ title }}<br /><em>{{ subtitle }}</em></h1>
        <p class="hero-copy">{{ hero_copy }}</p>
      </div>
      <div class="hero-note">
        <span class="hero-note-icon">✦</span>
        <span>{{ hero_note }}<br /><strong>{{ hero_note_subtitle }}</strong></span>
      </div>
    </section>

    <section class="explore-section planner-section" id="planner" aria-labelledby="route-title">
      <div class="section-heading">
        <div>
          <p class="eyebrow dark-eyebrow"><span class="eyebrow-line"></span>{{ route }}</p>
          <h2 id="route-title">{{ title }}<br /><em>{{ generate }}</em></h2>
        </div>
        <p class="section-intro">{{ planner_intro }}</p>
      </div>

    <form class="planner-form" method="post" action="/dashboard/plan?lang={{ selected_language }}">
      <input type="hidden" name="language" value="{{ selected_language }}">

      <div class="planner-field">
        <label for="country">{{ country }}</label>
        <select id="country" name="country" required>
          <option value="" disabled {% if not selected_country %}selected{% endif %}>{{ country_placeholder }}</option>
          {% for country_option in countries %}
          <option value="{{ country_option }}" {% if selected_country == country_option %}selected{% endif %}>{{ country_option }}</option>
          {% endfor %}
        </select>
      </div>

      <div class="planner-field">
        <label for="destination">{{ destination }}</label>
        <select id="destination" name="destination" required>
          <option value="" disabled {% if not selected_destination %}selected{% endif %}>{{ destination_placeholder }}</option>
          {% for place in destinations %}
          <option value="{{ place.name }}" {% if selected_destination == place.name %}selected{% endif %}>{{ place.name }}</option>
          {% endfor %}
        </select>
      </div>

      <div class="planner-field">
        <label for="depart-date">{{ depart_date }}</label>
        <input id="depart-date" type="date" name="depart_date" value="{{ selected_depart_date }}" min="{{ min_depart_date }}" required>
      </div>

      <div class="planner-field">
        <label for="return-date">{{ return_date }}</label>
        <input id="return-date" type="date" name="return_date" value="{{ selected_return_date }}" min="{{ min_return_date }}" required>
      </div>

      <div class="planner-field">
        <label for="season">{{ season }}</label>
        <select id="season" name="season">
          <option value="" {% if not selected_season %}selected{% endif %}>{{ any_season }}</option>
          <option value="spring" {% if selected_season == "spring" %}selected{% endif %}>{{ season_spring }}</option>
          <option value="summer" {% if selected_season == "summer" %}selected{% endif %}>{{ season_summer }}</option>
          <option value="autumn" {% if selected_season == "autumn" %}selected{% endif %}>{{ season_autumn }}</option>
          <option value="winter" {% if selected_season == "winter" %}selected{% endif %}>{{ season_winter }}</option>
        </select>
      </div>

      <div class="planner-submit">
        <button class="search-button" type="submit">{{ search }} <span>→</span></button>
      </div>
    </form>

    <section class="planner-places" id="place-gallery" aria-labelledby="places-title">
      <div class="planner-places-heading">
        <p class="eyebrow dark-eyebrow"><span class="eyebrow-line"></span>{{ places_eyebrow }}</p>
        <h2 id="places-title">{{ places_title }}</h2>
      </div>
      <div class="planner-places-grid">
        {% for place in nepal_places %}
        <article class="planner-place-card">
          <img src="{{ place.image }}" alt="{{ place.name }}" loading="lazy">
          <h3>{{ place.name }}</h3>
        </article>
        {% endfor %}
      </div>
    </section>

    <dialog class="destination-dialog" id="destination-dialog" aria-labelledby="destination-preview-title">
      <button class="destination-dialog-close" id="destination-dialog-close" type="button" aria-label="{{ dialog_close }}">×</button>
      <div class="destination-preview">
        <img id="destination-preview-image" src="" alt="">
        <div class="destination-preview-content">
          <p class="eyebrow dark-eyebrow"><span class="eyebrow-line"></span>{{ dialog_country }}</p>
          <h2 id="destination-preview-title"></h2>
          <dl class="destination-preview-facts">
            <div><dt>{{ dialog_country }}</dt><dd id="destination-preview-country"></dd></div>
            <div><dt>{{ dialog_region }}</dt><dd id="destination-preview-region"></dd></div>
            <div><dt>{{ dialog_daily_cost }}</dt><dd id="destination-preview-daily"></dd></div>
            <div><dt>{{ dialog_trip_cost }}</dt><dd id="destination-preview-trip"></dd></div>
            <div><dt>{{ dialog_flight_cost }}</dt><dd id="destination-preview-flight"></dd></div>
            <div><dt>{{ dialog_total }}</dt><dd id="destination-preview-total"></dd></div>
          </dl>
          <p id="destination-preview-description"></p>
          <p><strong>{{ dialog_best_for }}:</strong> <span id="destination-preview-best-for"></span></p>
          <p><strong>{{ dialog_interests }}:</strong> <span id="destination-preview-interests"></span></p>
          <p class="destination-preview-note">{{ dialog_estimate_note }}</p>
          <button class="search-button" id="destination-dialog-close-action" type="button">{{ dialog_close }}</button>
        </div>
      </div>
    </dialog>

    {% if result %}
    <section class="planner-results" id="results" aria-labelledby="results-title">
      <div class="planner-results-heading">
        <div>
          <p class="eyebrow dark-eyebrow"><span class="eyebrow-line"></span>{{ ai }}</p>
          <h2 id="results-title">{{ trip_suggestions }}</h2>
        </div>
        <p class="planner-trip-summary">{{ selected_country }} · {{ selected_destination }} · {{ selected_depart_date }} → {{ selected_return_date }} · {{ trip_days_count }} days<br />{{ result.message }}{% if result.grand_total is defined %}<br /><strong>{{ dialog_trip_cost }}:</strong> ${{ "{:,.0f}".format(result.trip_cost) }}<br /><strong>{{ dialog_flight_cost }}:</strong> ${{ "{:,.0f}".format(result.flight_cost) }}<br /><strong>{{ dialog_total }}:</strong> ${{ "{:,.0f}".format(result.grand_total) }}{% endif %}</p>
      </div>
      <div class="planner-result-grid">

      {% for item in result.recommendations %}
      <article class="planner-result-card">
        {% set image_src = item.image if item.image is defined else item.image_url %}
        <img class="destination-image" src="{{ image_src }}" alt="{{ item.name }}" />
        <h3>{{ item.name }}</h3>
        <p class="planner-result-meta">{{ item.region }} · {{ daily_cost }} ${{ item.daily_cost }} · {{ total }} ${{ item.estimated_total }}</p>
        <p>{{ item.description }}</p>
        <p class="planner-result-tags"><strong>{{ best_for }}:</strong> {{ ', '.join(item.best_for) }}</p>
      </article>
      {% endfor %}
      </div>
    </section>
    </div>
    {% endif %}
    </section>
  </main>
  <footer class="planner-footer"><span>© 2025 Himalaya</span><a href="/">{{ footer_explore }}</a></footer>

  <script>
    const plannerMenuToggle = document.querySelector('#planner-menu-toggle');
    const plannerNav = document.querySelector('#planner-nav');
    const departDateInput = document.querySelector('#depart-date');
    const returnDateInput = document.querySelector('#return-date');
    const plannerForm = document.querySelector('.planner-form');
    const countrySelect = document.querySelector('#country');
    const destinationSelect = document.querySelector('#destination');
    const destinationDialog = document.querySelector('#destination-dialog');
    const destinationGallery = document.querySelector('#place-gallery');
    const destinationCatalog = {{ destination_catalog|tojson|safe }};
    const destinationDetailTranslations = {{ destination_detail_translations|tojson|safe }};
    const airfareByCountry = {{ airfare_by_country|tojson|safe }};
    const domesticFlightByDestination = {{ domestic_flight_by_destination|tojson|safe }};
    const plannerCopy = {
      datesNote: {{ dialog_dates_note|tojson|safe }},
      dailyCost: {{ dialog_daily_cost|tojson|safe }},
      tripCost: {{ dialog_trip_cost|tojson|safe }},
      flightCost: {{ dialog_flight_cost|tojson|safe }},
      total: {{ dialog_total|tojson|safe }},
      bestFor: {{ dialog_best_for|tojson|safe }},
      interests: {{ dialog_interests|tojson|safe }}
    };
    plannerMenuToggle.addEventListener('click', () => {
      const isOpen = plannerNav.classList.toggle('open');
      plannerMenuToggle.setAttribute('aria-expanded', String(isOpen));
      plannerMenuToggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });

    function changeDashboardLanguage(language) {
      const params = new URLSearchParams(new FormData(plannerForm));
      params.set('lang', language);
      window.location.href = `${window.location.pathname}?${params.toString()}`;
    }

    function displayMoney(amount) {
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(amount);
    }

    function setPreviewValue(id, value) {
      document.querySelector(id).textContent = value;
    }

    function showDestinationPreview() {
      const destination = destinationCatalog.find((place) => place.name === destinationSelect.value);
      const country = countrySelect.value;
      if (!destination || !country) return;

      const departDate = departDateInput.value ? new Date(`${departDateInput.value}T00:00:00Z`) : null;
      const returnDate = returnDateInput.value ? new Date(`${returnDateInput.value}T00:00:00Z`) : null;
      const days = departDate && returnDate && returnDate > departDate
        ? Math.round((returnDate - departDate) / 86400000)
        : 0;
      const tripCost = destination.daily_cost * days;
      const airfare = (airfareByCountry[country] || 0) + (domesticFlightByDestination[destination.name] || 0);
      const image = document.querySelector('#destination-preview-image');
      const localizedDetails = destinationDetailTranslations[destination.name] || {};

      image.src = destination.image_url;
      image.alt = destination.name;
      setPreviewValue('#destination-preview-title', destination.name);
      setPreviewValue('#destination-preview-country', country);
      setPreviewValue('#destination-preview-region', localizedDetails.region || destination.region);
      setPreviewValue('#destination-preview-daily', displayMoney(destination.daily_cost));
      setPreviewValue('#destination-preview-trip', days ? displayMoney(tripCost) : plannerCopy.datesNote);
      setPreviewValue('#destination-preview-flight', displayMoney(airfare));
      setPreviewValue('#destination-preview-total', displayMoney(tripCost + airfare));
      setPreviewValue('#destination-preview-description', localizedDetails.description || destination.description);
      setPreviewValue('#destination-preview-best-for', (localizedDetails.best_for || destination.best_for).join(', '));
      setPreviewValue('#destination-preview-interests', (localizedDetails.interests || destination.interests).join(', '));
      destinationGallery.hidden = true;
      if (!destinationDialog.open) destinationDialog.showModal();
    }

    countrySelect.addEventListener('change', showDestinationPreview);
    destinationSelect.addEventListener('change', showDestinationPreview);
    if (countrySelect.value && destinationSelect.value) showDestinationPreview();
    destinationDialog.addEventListener('close', () => { destinationGallery.hidden = false; });
    document.querySelector('#destination-dialog-close').addEventListener('click', () => destinationDialog.close());
    document.querySelector('#destination-dialog-close-action').addEventListener('click', () => destinationDialog.close());

    departDateInput.addEventListener('change', () => {
      if (!departDateInput.value) return;
      const nextDay = new Date(`${departDateInput.value}T00:00:00Z`);
      nextDay.setUTCDate(nextDay.getUTCDate() + 1);
      returnDateInput.min = nextDay.toISOString().slice(0, 10);
      if (returnDateInput.value && returnDateInput.value < returnDateInput.min) {
        returnDateInput.value = '';
      }
      if (destinationDialog.open) showDestinationPreview();
    });
    returnDateInput.addEventListener('change', () => {
      if (destinationDialog.open) showDestinationPreview();
    });
  </script>
</body>
</html>
"""


@planner_pages.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(Path(__file__).resolve().parent / "images", filename)


def render_dashboard(selected_language, result=None, **form_values):
    today = date.today()
    selected_depart_date = form_values.get("selected_depart_date", "")
    min_return_date = (today + timedelta(days=1)).isoformat()
    try:
        departure_date = date.fromisoformat(selected_depart_date)
        if departure_date >= today:
            min_return_date = (departure_date + timedelta(days=1)).isoformat()
    except ValueError:
        pass

    context = {
        "result": result,
        "selected_language": selected_language,
        "user_name": session.get("user_name", ""),
        "countries": COUNTRIES,
        "destinations": DESTINATION_CATALOG,
        "destination_catalog": DESTINATION_CATALOG,
        "destination_detail_translations": DESTINATION_DETAIL_TRANSLATIONS.get(selected_language, {}),
        "airfare_by_country": COUNTRY_AIRFARE_ESTIMATES_USD,
        "domestic_flight_by_destination": DESTINATION_FLIGHT_ESTIMATES_USD,
        "nepal_places": NEPAL_PLACES,
        "selected_country": "",
        "selected_destination": "",
        "selected_depart_date": "",
        "selected_return_date": "",
        "min_depart_date": today.isoformat(),
        "min_return_date": min_return_date,
        "selected_season": "",
        "trip_days_count": "",
    }
    context.update(form_values)
    context.update(get_translation(selected_language))
    return render_template_string(HTML, **context)


def get_form_values(source):
    return {
        "selected_country": source.get("country", ""),
        "selected_destination": source.get("destination", ""),
        "selected_depart_date": source.get("depart_date", ""),
        "selected_return_date": source.get("return_date", ""),
        "selected_season": source.get("season", ""),
    }


@planner_pages.route("/", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect("/signin.html")
    selected_language = request.args.get("lang") or request.form.get("language") or "en"
    return render_dashboard(selected_language, **get_form_values(request.args))


@planner_pages.route("/plan", methods=["GET", "POST"])
def plan_trip():
    if "user_id" not in session:
        return redirect("/signin.html")
    selected_language = request.args.get("lang") or request.form.get("language") or "en"
    submitted_values = request.form if request.method == "POST" else request.args
    if request.method == "GET" and not submitted_values.get("destination"):
      return render_dashboard(selected_language, **get_form_values(submitted_values))

    selected_country = submitted_values.get("country", "").strip()
    selected_destination = submitted_values.get("destination", "").strip()
    selected_depart_date = submitted_values.get("depart_date", "").strip()
    selected_return_date = submitted_values.get("return_date", "").strip()
    selected_season = submitted_values.get("season", "").strip().lower()
    result = None
    trip_days_count = ""
    today = date.today()
    min_depart_date = today.isoformat()
    min_return_date = (today + timedelta(days=1)).isoformat()
    flight_cost = 0
    translations = get_translation(selected_language)

    if selected_depart_date:
        try:
            departure_date = date.fromisoformat(selected_depart_date)
            if departure_date < today:
                result = {"recommendations": [], "estimated_total": 0, "message": translations["error_past_date"]}
            else:
                min_return_date = (departure_date + timedelta(days=1)).isoformat()
        except ValueError:
            result = {"recommendations": [], "estimated_total": 0, "message": translations["error_invalid_date"]}

    if result is None and selected_country not in COUNTRIES:
        result = {"recommendations": [], "estimated_total": 0, "message": translations["error_country"]}
    if result is None and selected_destination not in {place["name"] for place in planner.destinations}:
        result = {"recommendations": [], "estimated_total": 0, "message": translations["error_destination"]}

    if result is None:
        try:
            depart_date = date.fromisoformat(selected_depart_date)
            return_date = date.fromisoformat(selected_return_date)
            if return_date <= depart_date:
                raise ValueError
            trip_days_count = (return_date - depart_date).days
        except ValueError:
            result = {"recommendations": [], "estimated_total": 0, "message": translations["error_invalid_date"]}

    if result is None:
        flight_cost = COUNTRY_AIRFARE_ESTIMATES_USD[selected_country] + DESTINATION_FLIGHT_ESTIMATES_USD.get(selected_destination, 0)

    if result is None:
        result = planner.generate_itinerary(
            days=trip_days_count,
        budget_usd=None,
            region="",
            interests=[],
            season=selected_season,
            destination_name=selected_destination,
        )
        if result["recommendations"]:
            result["trip_cost"] = result["estimated_total"]
            result["flight_cost"] = flight_cost
            result["grand_total"] = result["trip_cost"] + flight_cost
            result["message"] = translations["results_found"]
            localized_details = DESTINATION_DETAIL_TRANSLATIONS.get(selected_language, {}).get(selected_destination)
            if localized_details:
                result["recommendations"][0].update(localized_details)
        else:
            result["message"] = translations["no_matches"]

    return render_dashboard(
        selected_language,
        result,
        selected_country=selected_country,
        selected_destination=selected_destination,
        selected_depart_date=selected_depart_date,
        selected_return_date=selected_return_date,
        min_depart_date=min_depart_date,
        min_return_date=min_return_date,
        selected_season=selected_season,
        trip_days_count=trip_days_count,
    )


@planner_pages.post("/signout")
def planner_signout():
    session.clear()
    return redirect("/signin.html")
