from services.top_k_analyzer import TopKAnalyzer

class TripAnalyzer:

    def __init__(self, trips):
        self.trips = trips

    def get_total_trips(self):
        return len(self.trips)

    def get_completed_trips(self):
        return sum(
            1
            for trip in self.trips
            if trip.is_completed()
        )

    def get_cancelled_trips(self):
        return sum(
            1
            for trip in self.trips
            if trip.status.lower() == "cancelled"
        )

    def get_total_revenue(self):
        return sum(
            trip.fare
            for trip in self.trips
            if trip.is_completed()
            and trip.fare is not None
            and trip.fare > 0
        )

    def get_average_fare(self):
        fares = [
            trip.fare
            for trip in self.trips
            if trip.fare is not None
            and trip.fare >= 0
        ]

        if not fares:
            return 0

        return sum(fares) / len(fares)

    def get_average_distance(self):
        distances = [
            trip.distance_km
            for trip in self.trips
            if trip.distance_km is not None
            and trip.distance_km >= 0
        ]

        if not distances:
            return 0

        return sum(distances) / len(distances)

    def get_average_duration(self):
        durations = [
            trip.calculate_duration()
            for trip in self.trips
            if trip.calculate_duration() is not None
            and trip.calculate_duration() >= 0
        ]

        if not durations:
            return 0

        return sum(durations) / len(durations)

    def get_completion_rate(self):
        total_trips = self.get_total_trips()

        if total_trips == 0:
            return 0

        return (
            self.get_completed_trips()
            / total_trips
        ) * 100

    def get_total_riders(self):
        riders = {
            trip.rider_id
            for trip in self.trips
            if trip.rider_id is not None
        }

        return len(riders)

    def get_cancellation_rate(self):
        total_trips = self.get_total_trips()

        if total_trips == 0:
            return 0

        return (
            self.get_cancelled_trips()
            / total_trips
        ) * 100

    def get_rider_trip_counts(self):

        rider_counts = {}

        for trip in self.trips:

            rider_id = trip.rider_id

            if rider_id is None:
                continue

            rider_counts[rider_id] = (
            rider_counts.get(rider_id, 0) + 1
        )

        return rider_counts

    def get_top_riders(self, k=5):

        rider_counts = self.get_rider_trip_counts()

        riders = [
            {
                "rider_id": rider_id,
                "trip_count": trip_count
            }
            for rider_id, trip_count
            in rider_counts.items()
        ]

        return TopKAnalyzer.top_k(
            riders,
            metric_function=lambda x: x["trip_count"],
            k=k
        )


    def get_dashboard_metrics(self):
        return {
            "total_trips": self.get_total_trips(),
            "completed_trips": self.get_completed_trips(),
            "cancelled_trips": self.get_cancelled_trips(),
            "total_riders": self.get_total_riders(),
            "completion_rate": self.get_completion_rate(),
            "cancellation_rate": self.get_cancellation_rate(),
            "total_revenue": self.get_total_revenue(),
            "average_fare": self.get_average_fare(),
            "average_distance": self.get_average_distance(),
            "average_duration": self.get_average_duration()
        }