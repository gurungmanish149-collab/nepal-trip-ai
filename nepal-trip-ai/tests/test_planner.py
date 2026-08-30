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
    assert any(item["name"] == "Kathmandu" for item in result["recommendations"])
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
    assert any(item["name"] in {"Pokhara", "Everest Base Camp Region"} for item in result["recommendations"])


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
