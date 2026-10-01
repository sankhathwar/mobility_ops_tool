from services.data_loader import DataLoader
from services.cancellation_analyzer import CancellationAnalyzer


loader = DataLoader()

trips = loader.load_trips("data/Trips.csv")

analyzer = CancellationAnalyzer(trips)


print("\nTOTAL CANCELLATIONS")
print("=" * 40)
print(analyzer.get_total_cancellations())


print("\nCANCELLATIONS BY REASON")
print("=" * 40)
print(analyzer.get_cancellations_by_reason())


print("\nCANCELLATIONS BY ZONE")
print("=" * 40)
print(analyzer.get_cancellations_by_zone())


print("\nCANCELLATIONS BY DRIVER")
print("=" * 40)
print(analyzer.get_cancellations_by_driver())


print("\nCANCELLATIONS BY TIME")
print("=" * 40)
print(analyzer.get_cancellations_by_time())


print("\nFULL SUMMARY")
print("=" * 40)
print(analyzer.get_cancellation_summary())