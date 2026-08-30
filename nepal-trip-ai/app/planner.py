from typing import List, Dict, Any

from app.data import DESTINATIONS


class TravelPlanner:
    def __init__(self):
        self.destinations = DESTINATIONS

    def matches_region(self, destination: Dict[str, Any], region: str) -> bool:
        normalized = (region or "").strip().lower()
        if not normalized or normalized in {"any", "all", "select"}:
            return True
        return destination["region"].lower() == normalized

    def matches_interest(self, destination: Dict[str, Any], interests: List[str]) -> bool:
        if not interests:
            return True
        normalized = {item.lower() for item in interests}
        return bool(normalized.intersection({item.lower() for item in destination["interests"]}))

    def matches_season(self, destination: Dict[str, Any], season: str) -> bool:
        normalized = (season or "").strip().lower()
        if not normalized or normalized in {"any", "all", "select"}:
            return True
        return normalized in {item.lower() for item in destination["season"]}

    def generate_itinerary(
        self,
        days: int,
        budget_usd: int,
        region: str,
        interests: List[str],
        season: str,
    ) -> Dict[str, Any]:
        recommendations = []

        for destination in self.destinations:
            estimated_total = destination["daily_cost"] * days
            if estimated_total > budget_usd:
                continue
            if not self.matches_region(destination, region):
                continue
            if not self.matches_interest(destination, interests):
                continue
            if not self.matches_season(destination, season):
                continue

            recommendations.append(
                {
                    "name": destination["name"],
                    "region": destination["region"],
                    "daily_cost": destination["daily_cost"],
                    "estimated_total": estimated_total,
                    "interests": destination["interests"],
                    "best_for": destination["best_for"],
                    "description": destination["description"],
                    "image_url": destination.get("image_url", ""),
                    "image": destination.get("image_url", ""),
                }
            )

        if not recommendations:
            return {
                "recommendations": [],
                "estimated_total": 0,
                "message": "No destinations match your current filters. Try a wider budget or different travel interests.",
            }

        recommendations.sort(key=lambda item: item["estimated_total"])

        total = sum(item["estimated_total"] for item in recommendations)
        return {
            "recommendations": recommendations[:3],
            "estimated_total": total,
            "message": f"Found {len(recommendations)} matching destinations for your trip.",
        }
