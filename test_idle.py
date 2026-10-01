from services.data_loader import DataLoader
from services.idle_time_analyzer import IdleTimeAnalyzer


loader = DataLoader()

trips = loader.load_trips("data/Trips.csv")

analyzer = IdleTimeAnalyzer(trips)


driver_ids = sorted(
    set(trip.driver_id for trip in trips)
)


print("\nIDLE TIME ANALYSIS")
print("=" * 60)

for driver_id in driver_ids:

    result = analyzer.get_driver_idle_summary(
        driver_id,
        threshold_minutes=60
    )

    print(f"\nDriver: {driver_id}")
    print(f"Total Idle Gaps: {result['total_idle_gaps']}")
    print(f"Long Idle Periods: {result['long_idle_periods']}")

    for gap in result["idle_gaps"]:
        print(
            f"  {gap['previous_trip_id']} -> "
            f"{gap['next_trip_id']}: "
            f"{gap['idle_minutes']} minutes"
        )


print("\nCUSTOM THRESHOLD TEST")
print("=" * 60)

driver_id = driver_ids[0]

result = analyzer.get_driver_idle_summary(
    driver_id,
    threshold_minutes=30
)

print(result)