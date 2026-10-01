from services.data_loader import DataLoader
from services.utilization_analyzer import UtilizationAnalyzer
from services.anomaly_detector import AnomalyDetector


loader = DataLoader()

drivers = loader.load_drivers("data/Drivers.csv")
trips = loader.load_trips("data/Trips.csv")
activities = loader.load_driver_activity(
    "data/Driver_activity.csv"
)

utilization_analyzer = UtilizationAnalyzer(
    activities,
    trips
)

detector = AnomalyDetector(
    drivers,
    trips,
    utilization_analyzer
)


print("\nTRIP ANOMALIES")
print("=" * 60)

print(
    "Negative Fares:",
    len(detector.detect_negative_fares())
)

print(
    "Zero Distance:",
    len(detector.detect_zero_distance())
)

print(
    "Invalid Timestamps:",
    len(detector.detect_invalid_timestamps())
)

print(
    "Long Duration:",
    len(detector.detect_long_duration())
)

print(
    "Unknown Drivers:",
    len(detector.detect_unknown_drivers())
)

print(
    "Unusual Fares:",
    len(detector.detect_unusual_fares())
)


print("\nDRIVER ANOMALIES")
print("=" * 60)

print(
    "High Cancellation Rate:",
    detector.detect_high_cancellation_rate()
)

print(
    "Low Utilization:",
    detector.detect_low_utilization()
)

print(
    "High Trip Count:",
    detector.detect_high_trip_count()
)

print(
    "Low Rating:",
    detector.detect_low_rating()
)


print("\nCOMPLETE ANOMALY SUMMARY")
print("=" * 60)

summary = detector.get_all_anomalies()

for anomaly_type, results in summary.items():
    print(
        f"{anomaly_type}: {len(results)}"
    )