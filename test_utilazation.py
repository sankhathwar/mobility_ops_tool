from services.data_loader import DataLoader
from services.utilization_analyzer import UtilizationAnalyzer


loader = DataLoader()

trips = loader.load_trips("data/Trips.csv")
activities = loader.load_driver_activity("data/Driver_activity.csv")

analyzer = UtilizationAnalyzer(activities, trips)


driver_ids = sorted(
    set(activity.driver_id for activity in activities)
)


print("\nDRIVER UTILIZATION")
print("=" * 60)

for driver_id in driver_ids:

    result = analyzer.get_driver_utilization(driver_id)

    print(f"\nDriver: {driver_id}")
    print(f"Online Hours: {result['online_hours']}")
    print(f"Busy Hours: {result['busy_hours']}")
    print(f"Idle Hours: {result['idle_hours']}")
    print(f"Utilization: {result['utilization']}%")
    print(f"Classification: {result['classification']}")


print("\nCUSTOM THRESHOLD TEST")
print("=" * 60)

driver_id = driver_ids[0]

result = analyzer.get_driver_utilization(
    driver_id,
    high_threshold=80,
    medium_threshold=50
)

print(result)