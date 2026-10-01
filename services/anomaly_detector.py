class AnomalyDetector:

    def __init__(
        self,
        drivers,
        trips,
        utilization_analyzer=None
    ):
        self.drivers = drivers
        self.trips = trips
        self.utilization_analyzer = utilization_analyzer

        self.driver_ids = {
            driver.driver_id
            for driver in drivers
        }

    # -------------------------
    # TRIP ANOMALIES
    # -------------------------

    def detect_negative_fares(self):
        return [
            trip
            for trip in self.trips
            if trip.fare is not None and trip.fare < 0
        ]

    def detect_zero_distance(self):
        return [
            trip
            for trip in self.trips
            if trip.distance_km is not None
            and trip.distance_km <= 0
        ]

    def detect_invalid_timestamps(self):
        anomalies = []

        for trip in self.trips:

            if trip.request_time is None:
                anomalies.append(trip)
                continue

            if trip.is_completed():

                if (
                    trip.pickup_time is None
                    or trip.drop_time is None
                ):
                    anomalies.append(trip)
                    continue

                if trip.pickup_time < trip.request_time:
                    anomalies.append(trip)
                    continue

                if trip.drop_time < trip.pickup_time:
                    anomalies.append(trip)

        return anomalies

    def detect_long_duration(self, threshold_minutes=120):
        anomalies = []

        for trip in self.trips:

            duration = trip.calculate_duration()

            if (
                duration is not None
                and duration > threshold_minutes
            ):
                anomalies.append(trip)

        return anomalies

    def detect_unknown_drivers(self):
        return [
            trip
            for trip in self.trips
            if trip.driver_id not in self.driver_ids
        ]

    def detect_unusual_fares(
        self,
        minimum_fare=50,
        maximum_fare=1000
    ):
        return [
            trip
            for trip in self.trips
            if trip.fare is not None
            and (
                trip.fare < minimum_fare
                or trip.fare > maximum_fare
            )
        ]

    # -------------------------
    # DRIVER ANOMALIES
    # -------------------------

    def detect_high_cancellation_rate(
        self,
        threshold=30
    ):
        anomalies = []

        for driver in self.drivers:

            driver_trips = [
                trip
                for trip in self.trips
                if trip.driver_id == driver.driver_id
            ]

            if not driver_trips:
                continue

            cancelled = sum(
                1
                for trip in driver_trips
                if trip.status.lower() == "cancelled"
            )

            cancellation_rate = (
                cancelled / len(driver_trips)
            ) * 100

            if cancellation_rate >= threshold:
                anomalies.append({
                    "driver_id": driver.driver_id,
                    "cancellation_rate": round(
                        cancellation_rate,
                        2
                    )
                })

        return anomalies

    def detect_low_utilization(
        self,
        threshold=20
    ):
        if self.utilization_analyzer is None:
            return []

        anomalies = []

        for driver in self.drivers:

            utilization = (
                self.utilization_analyzer
                .calculate_utilization(driver.driver_id)
            )

            if utilization < threshold:
                anomalies.append({
                    "driver_id": driver.driver_id,
                    "utilization": utilization
                })

        return anomalies

    def detect_high_trip_count(
        self,
        threshold=10
    ):
        anomalies = []

        for driver in self.drivers:

            trip_count = sum(
                1
                for trip in self.trips
                if trip.driver_id == driver.driver_id
            )

            if trip_count >= threshold:
                anomalies.append({
                    "driver_id": driver.driver_id,
                    "trip_count": trip_count
                })

        return anomalies

    def detect_low_rating(self, threshold=4.0):
        return [
            {
                "driver_id": driver.driver_id,
                "rating": driver.rating
            }
            for driver in self.drivers
            if driver.rating < threshold
        ]

    # -------------------------
    # COMPLETE SUMMARY
    # -------------------------

    def get_all_anomalies(self):
        return {
            "negative_fares": self.detect_negative_fares(),
            "zero_distance": self.detect_zero_distance(),
            "invalid_timestamps": self.detect_invalid_timestamps(),
            "long_duration": self.detect_long_duration(),
            "unknown_drivers": self.detect_unknown_drivers(),
            "unusual_fares": self.detect_unusual_fares(),
            "high_cancellation_rate":
                self.detect_high_cancellation_rate(),
            "low_utilization":
                self.detect_low_utilization(),
            "high_trip_count":
                self.detect_high_trip_count(),
            "low_rating":
                self.detect_low_rating()
        }