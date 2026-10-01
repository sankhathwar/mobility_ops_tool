import pandas as pd

from services.data_loader import DataLoader
from services.driver_analyzer import DriverAnalyzer
from services.trip_analyzer import TripAnalyzer
from services.dashboard_analyzer import DashboardAnalyzer


loader = DataLoader()

drivers = loader.load_drivers(
    "data/Drivers.csv"
)

trips = loader.load_trips(
    "data/Trips.csv"
)


driver_analyzer = DriverAnalyzer(
    drivers, trips
)

trip_analyzer = TripAnalyzer(
    trips
)


dashboard_analyzer = DashboardAnalyzer(
    driver_analyzer,
    trip_analyzer
)


kpis = dashboard_analyzer.get_kpis()


print("\nDASHBOARD KPIs")
print("=" * 50)

for key, value in kpis.items():
    print(f"{key}: {value}")