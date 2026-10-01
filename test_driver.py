from services.data_loader import DataLoader
from services.driver_analyzer import DriverAnalyzer


loader = DataLoader()

drivers = loader.load_drivers(
    "data/Drivers.csv"
)

trips = loader.load_trips(
    "data/Trips.csv"
)

analyzer = DriverAnalyzer(
    drivers,
    trips
)


driver_id = "D102"

result = analyzer.get_driver_performance(
    driver_id
)


print("\nDRIVER PERFORMANCE")
print("=" * 50)

for key, value in result.items():
    print(f"{key}: {value}")

print("\nHASH-MAP LOOKUP")
print("=" * 50)

driver = analyzer.get_driver("D102")

print(driver.get_profile())

driver = analyzer.get_driver("D999")

print(driver)

print("\nTOP DRIVERS BY COMPLETED TRIPS")
print("=" * 50)

top_drivers = analyzer.get_top_drivers_by_completed_trips(3)

for driver in top_drivers:
    print(
        driver["driver_id"],
        driver["driver_name"],
        driver["completed_trips"]
    )


print("\nHIGHEST REVENUE DRIVERS")
print("=" * 50)

revenue_drivers = analyzer.get_highest_revenue_drivers(3)

for driver in revenue_drivers:
    print(
        driver["driver_id"],
        driver["driver_name"],
        driver["revenue"]
    )


print("\nLOWEST CANCELLATION DRIVERS")
print("=" * 50)

low_cancel_drivers = (
    analyzer.get_lowest_cancellation_drivers(3)
)

for driver in low_cancel_drivers:
    print(
        driver["driver_id"],
        driver["driver_name"],
        driver["cancellation_rate"]
    )