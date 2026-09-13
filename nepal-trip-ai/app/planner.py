from datetime import datetime
from typing import List, Dict, Any

from app.data import DESTINATIONS


class TravelPlanner:
    COUNTRY_FLIGHT_BASE_JPY = {
        "japan": 98000,
        "korea": 76000,
        "china": 68000,
        "australia": 142000,
        "america": 188000,
        "default": 110000,
    }

    DESTINATION_REGION_FACTOR = {
        "central": 1.0,
        "eastern": 1.08,
        "western": 1.12,
        "northern": 1.2,
        "southern": 0.96,
    }

    def __init__(self):
        self.destinations = DESTINATIONS

    @staticmethod
    def normalize_text(value: str) -> str:
        return (value or "").strip().lower().replace("-", " ").replace("_", " ")

    @staticmethod
    def normalize_country(value: str) -> str:
        return TravelPlanner.normalize_text(value)

    @staticmethod
    def parse_trip_days(departure_date: str, return_date: str) -> int:
        for date_format in ("%Y-%m-%d", "%Y/%m/%d"):
            try:
                departure = datetime.strptime(departure_date, date_format)
                arrival = datetime.strptime(return_date, date_format)
                delta = (arrival - departure).days + 1
                return max(1, delta)
            except ValueError:
                continue
        return 1

    def find_destination(self, destination_name: str) -> Dict[str, Any]:
        target_name = self.normalize_text(destination_name)
        for destination in self.destinations:
            if self.normalize_text(destination["name"]) == target_name:
                return destination
        for destination in self.destinations:
            if target_name in self.normalize_text(destination["name"]):
                return destination
        raise ValueError(f"Destination not found: {destination_name}")

    def estimate_airfare_jpy(self, from_country: str, destination_name: str) -> int:
        destination = self.find_destination(destination_name)
        country_key = self.normalize_country(from_country)
        base_rate = self.COUNTRY_FLIGHT_BASE_JPY.get(country_key, self.COUNTRY_FLIGHT_BASE_JPY["default"])
        region_factor = self.DESTINATION_REGION_FACTOR.get(destination["region"].lower(), 1.0)
        return int(round(base_rate * region_factor))

    def calculate_trip_cost(
        self,
        from_country: str,
        destination_name: str,
        departure_date: str,
        return_date: str,
    ) -> Dict[str, Any]:
        destination = self.find_destination(destination_name)
        trip_days = self.parse_trip_days(departure_date, return_date)
        airfare_jpy = self.estimate_airfare_jpy(from_country, destination["name"])
        local_expenses_jpy = int(round(destination["daily_cost"] * trip_days * 150))
        total_cost_jpy = airfare_jpy + local_expenses_jpy

        return {
            "from_country": from_country,
            "destination": destination["name"],
            "region": destination["region"],
            "departure_date": departure_date,
            "return_date": return_date,
            "trip_days": trip_days,
            "airfare_jpy": airfare_jpy,
            "local_expenses_jpy": local_expenses_jpy,
            "total_cost_jpy": total_cost_jpy,
            "currency": "JPY",
            "daily_cost_usd": destination["daily_cost"],
            "estimated_total_usd": destination["daily_cost"] * trip_days,
        }

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
