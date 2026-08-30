from app.planner import TravelPlanner


def parse_interests(raw_value: str):
    if not raw_value:
        return []
    return [item.strip().lower() for item in raw_value.split(",") if item.strip()]


def main():
    print("========================================")
    print("NepalTrip AI — Smart Nepal Travel Planner")
    print("========================================")

    days = int(input("How many days do you want to travel? [5]: ") or "5")
    budget = int(input("What is your total budget in USD? [500]: ") or "500")
    region = input("Preferred region? (Central, Western, Northern, Southern, Eastern, Any) [Any]: ") or "Any"
    interests = parse_interests(input("Interests? (culture, trekking, nature, wildlife, food, religion) [culture]: ") or "culture")
    season = (input("Season? (spring, summer, autumn, winter, any) [spring]: ") or "spring").lower()

    planner = TravelPlanner()
    result = planner.generate_itinerary(
        days=days,
        budget_usd=budget,
        region=region,
        interests=interests,
        season=season,
    )

    if not result["recommendations"]:
        print(result["message"])
        return

    print("\nRecommended destinations:")
    for index, item in enumerate(result["recommendations"], start=1):
        print(f"\n{index}. {item['name']} ({item['region']})")
        print(f"   Estimated total: ${item['estimated_total']}")
        print(f"   Daily budget: ${item['daily_cost']}")
        print(f"   Best for: {', '.join(item['best_for'])}")
        print(f"   Interests: {', '.join(item['interests'])}")
        print(f"   Description: {item['description']}")

    print(f"\nOverall estimated trip cost: ${result['estimated_total']}")
    print("\nThis app follows the flow: Travel Preferences → Python Backend → Destination Database → Route/Budget Calculation → Personalized Itinerary.")


if __name__ == "__main__":
    main()
