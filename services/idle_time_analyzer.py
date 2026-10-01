class IdleTimeAnalyzer:

    def __init__(self, trips):
        self.trips = trips

    def get_driver_trips(self, driver_id):
        driver_trips = [
            trip
            for trip in self.trips
            if trip.driver_id == driver_id
            and trip.is_completed()
            and trip.drop_time is not None
            and trip.pickup_time is not None
        ]

        return sorted(
            driver_trips,
            key=lambda x: x.pickup_time
        )

    def calculate_idle_gaps(self, driver_id):
        trips = self.get_driver_trips(driver_id)

        idle_gaps = []

        for i in range(len(trips) - 1):

            current_trip = trips[i]
            next_trip = trips[i + 1]

            gap = (
                next_trip.pickup_time -
                current_trip.drop_time
            )

            idle_minutes = gap.total_seconds() / 60

            idle_gaps.append({
                "previous_trip_id": current_trip.trip_id,
                "next_trip_id": next_trip.trip_id,
                "idle_minutes": round(idle_minutes, 2)
            })

        return idle_gaps

    def get_long_idle_periods(self, driver_id, threshold_minutes=60):
        idle_gaps = self.calculate_idle_gaps(driver_id)

        return [
            gap
            for gap in idle_gaps
            if gap["idle_minutes"] >= threshold_minutes
        ]

    def get_driver_idle_summary(
        self,
        driver_id,
        threshold_minutes=60
    ):
        idle_gaps = self.calculate_idle_gaps(driver_id)
        long_idle_periods = self.get_long_idle_periods(
            driver_id,
            threshold_minutes
        )

        return {
            "driver_id": driver_id,
            "total_idle_gaps": len(idle_gaps),
            "long_idle_periods": len(long_idle_periods),
            "idle_gaps": idle_gaps,
            "threshold_minutes": threshold_minutes
        }