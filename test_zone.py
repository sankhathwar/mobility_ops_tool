from services.data_loader import DataLoader
from services.zone_analyzer import ZoneAnalyzer


loader = DataLoader()

drivers = loader.load_drivers("data/Drivers.csv")
trips = loader.load_trips("data/Trips.csv")
activities = loader.load_driver_activity("data/Driver_activity.csv")

analyzer = ZoneAnalyzer(trips)


print("\nALL ZONES")
print("=" * 40)

zones = analyzer.get_zones()

for zone in zones:
    print(zone)


print("\nZONE METRICS")
print("=" * 40)

for zone in zones:
    metrics = analyzer.get_zone_metrics(zone)

    print(f"\nZone: {zone}")
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Completed Trips: {metrics['completed_trips']}")
    print(f"Cancelled Trips: {metrics['cancelled_trips']}")
    print(f"Completion Rate: {metrics['completion_rate']}%")
    print(f"Cancellation Rate: {metrics['cancellation_rate']}%")
    print(f"Revenue: {metrics['revenue']}")
    print(f"Average Fare: {metrics['average_fare']}")

    print("Demand Distribution:")
    for time_slot, count in metrics["demand_distribution"].items():
        print(f"  {time_slot}: {count}")


print("\nSINGLE ZONE TEST")
print("=" * 40)

zone = zones[0]

print("Selected Zone:", zone)
print(analyzer.get_zone_metrics(zone))