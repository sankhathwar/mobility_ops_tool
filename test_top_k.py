from services.data_loader import DataLoader
from services.trip_analyzer import TripAnalyzer
from services.top_k_analyzer import TopKAnalyzer


loader = DataLoader()

trips = loader.load_trips(
    "data/Trips.csv"
)

trip_analyzer = TripAnalyzer(trips)


# Check all rider counts
rider_counts = trip_analyzer.get_rider_trip_counts()

print("\nALL RIDER COUNTS")
print("=" * 40)

print(rider_counts)
print("Number of riders:", len(rider_counts))


# Check the list passed to TopK
riders = [
    {
        "rider_id": rider_id,
        "trip_count": trip_count
    }
    for rider_id, trip_count in rider_counts.items()
]

print("\nRIDER LIST")
print("=" * 40)

for rider in riders:
    print(rider)


# Directly test TopK
result = TopKAnalyzer.top_k(
    riders,
    metric_function=lambda x: x["trip_count"],
    k=5
)

print("\nTOP K RESULT")
print("=" * 40)

print(result)
print("Number of results:", len(result))


# Test through TripAnalyzer
top_riders = trip_analyzer.get_top_riders(5)

print("\nTOP RIDERS THROUGH ANALYZER")
print("=" * 40)

for rider in top_riders:
    print(
        rider["rider_id"],
        rider["trip_count"]
    )