import os
import sys

if __package__ in (None, ""):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from flask import Flask, render_template_string, request, send_from_directory

from app.planner import TravelPlanner

app = Flask(__name__, static_folder="static", static_url_path="/static")
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


@app.route("/", methods=["GET", "POST"])
def home():
    selected_language = request.args.get("lang") or request.form.get("language") or "en"
    texts = get_translation(selected_language)
    return render_template_string(HTML, result=None, selected_language=selected_language, **texts)


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
