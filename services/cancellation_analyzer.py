class CancellationAnalyzer:

    def __init__(self, trips):
        self.trips = trips

    def get_cancelled_trips(self):
        return [
            trip for trip in self.trips
            if trip.status.lower() == "cancelled"
        ]

    def get_total_cancellations(self):
        return len(self.get_cancelled_trips())

    def get_cancellations_by_reason(self):
        counts = {}

        for trip in self.get_cancelled_trips():
            reason = trip.cancellation_reason

            if not reason:
                reason = "Unknown"

            counts[reason] = counts.get(reason, 0) + 1

        return counts

    def get_cancellations_by_zone(self):
        counts = {}

        for trip in self.get_cancelled_trips():
            zone = trip.pickup_zone

            if not zone:
                zone = "Unknown"

            counts[zone] = counts.get(zone, 0) + 1

        return counts

    def get_cancellations_by_driver(self):
        counts = {}

        for trip in self.get_cancelled_trips():
            driver_id = trip.driver_id

            if not driver_id:
                driver_id = "Unknown"

            counts[driver_id] = counts.get(driver_id, 0) + 1

        return counts

    def get_cancellations_by_time(self):
        counts = {
            "06-09": 0,
            "09-12": 0,
            "12-15": 0,
            "15-18": 0,
            "18-21": 0,
            "21-00": 0
        }

        for trip in self.get_cancelled_trips():

            if trip.request_time is None:
                continue

            hour = trip.request_time.hour

            if 6 <= hour < 9:
                counts["06-09"] += 1

            elif 9 <= hour < 12:
                counts["09-12"] += 1

            elif 12 <= hour < 15:
                counts["12-15"] += 1

            elif 15 <= hour < 18:
                counts["15-18"] += 1

            elif 18 <= hour < 21:
                counts["18-21"] += 1

            elif 21 <= hour < 24:
                counts["21-00"] += 1

        return counts

    def get_cancellation_summary(self):
        return {
            "total_cancellations": self.get_total_cancellations(),
            "by_reason": self.get_cancellations_by_reason(),
            "by_zone": self.get_cancellations_by_zone(),
            "by_driver": self.get_cancellations_by_driver(),
            "by_time": self.get_cancellations_by_time()
        }