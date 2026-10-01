from app.planner import TravelPlanner


def test_recommend_destinations_for_culture_trip():
    planner = TravelPlanner()
    result = planner.generate_itinerary(
        days=5,
        budget_usd=450,
        region="Any",
        interests=["culture", "food"],
        season="spring",
    )

    assert result["recommendations"]
    assert any(item["interests"] and "culture" in item["interests"] for item in result["recommendations"])
    assert result["estimated_total"] > 0


def test_recommendation_for_trekking_budget():
    planner = TravelPlanner()
    result = planner.generate_itinerary(
        days=7,
        budget_usd=700,
        region="Any",
        interests=["trekking"],
        season="autumn",
    )

    assert result["recommendations"]
    assert any(item["interests"] and "trekking" in item["interests"] for item in result["recommendations"])


def test_no_matching_destinations_returns_empty_result():
    planner = TravelPlanner()
    result = planner.generate_itinerary(
        days=2,
        budget_usd=50,
        region="Northern",
        interests=["trekking"],
        season="winter",
    )

    assert result["recommendations"] == []
    assert "No destinations" in result["message"]


def test_japan_to_ilam_trip_cost_includes_flight_and_daily_expenses_in_jpy():
    planner = TravelPlanner()
    quote = planner.calculate_trip_cost("Japan", "Ilam", "2026-09-14", "2026-09-19")

    assert quote["from_country"] == "Japan"
    assert quote["destination"] == "Ilam"
    assert quote["trip_days"] == 6
    assert quote["airfare_jpy"] > 0
    assert quote["local_expenses_jpy"] > 0
    assert quote["total_cost_jpy"] == quote["airfare_jpy"] + quote["local_expenses_jpy"]


def test_china_to_kathmandu_trip_cost_includes_flight_and_daily_expenses_in_jpy():
    planner = TravelPlanner()
    quote = planner.calculate_trip_cost("China", "Kathmandu", "2026-09-14", "2026-09-19")

    assert quote["from_country"] == "China"
    assert quote["destination"] == "Kathmandu"
    assert quote["trip_days"] == 6
    assert quote["airfare_jpy"] > 0
    assert quote["local_expenses_jpy"] > 0
    assert quote["total_cost_jpy"] == quote["airfare_jpy"] + quote["local_expenses_jpy"]
