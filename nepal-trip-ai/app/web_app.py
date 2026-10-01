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
