from services.data_loader import DataLoader
from services.zone_analyzer import ZoneAnalyzer
from services.cancellation_analyzer import CancellationAnalyzer
from services.utilization_analyzer import UtilizationAnalyzer
from services.anomaly_detector import AnomalyDetector
from services.insights_engine import InsightsEngine


loader = DataLoader()

drivers = loader.load_drivers("data/Drivers.csv")
trips = loader.load_trips("data/Trips.csv")
activities = loader.load_driver_activity(
    "data/Driver_activity.csv"
)


zone_analyzer = ZoneAnalyzer(trips)

cancellation_analyzer = CancellationAnalyzer(trips)

utilization_analyzer = UtilizationAnalyzer(
    activities,
    trips
)

anomaly_detector = AnomalyDetector(
    drivers,
    trips,
    utilization_analyzer
)


insights_engine = InsightsEngine(
    zone_analyzer,
    cancellation_analyzer,
    anomaly_detector,
    utilization_analyzer,
    trips
)


print("\nGENERATED OPERATIONAL INSIGHTS")
print("=" * 60)

insights = insights_engine.generate_insights()

for insight, value in insights.items():
    print(f"{insight}: {value}")