class UtilizationAnalyzer:

    def __init__(self, activities, trips):
        self.activities = activities
        self.trips = trips

    def get_driver_activities(self, driver_id):
        driver_activities = [
            activity
            for activity in self.activities
            if activity.driver_id == driver_id
        ]

        return sorted(
            driver_activities,
            key=lambda x: x.timestamp
        )

    def calculate_online_hours(self, driver_id):
        activities = self.get_driver_activities(driver_id)

        online_hours = 0

        for i in range(len(activities) - 1):
            current = activities[i]
            next_activity = activities[i + 1]

            if current.is_online() and next_activity.is_offline():
                duration = next_activity.timestamp - current.timestamp
                online_hours += duration.total_seconds() / 3600

        return round(online_hours, 2)

    def calculate_busy_hours(self, driver_id):
        driver_trips = [
            trip for trip in self.trips
            if trip.driver_id == driver_id
            and trip.is_completed()
            and trip.pickup_time is not None
            and trip.drop_time is not None
        ]

        busy_hours = 0

        for trip in driver_trips:
            duration = trip.drop_time - trip.pickup_time
            busy_hours += duration.total_seconds() / 3600

        return round(busy_hours, 2)

    def calculate_idle_hours(self, driver_id):
        online_hours = self.calculate_online_hours(driver_id)
        busy_hours = self.calculate_busy_hours(driver_id)

        idle_hours = online_hours - busy_hours

        return round(max(idle_hours, 0), 2)

    def calculate_utilization(self, driver_id):
        online_hours = self.calculate_online_hours(driver_id)

        if online_hours == 0:
            return 0

        busy_hours = self.calculate_busy_hours(driver_id)

        return round(
            (busy_hours / online_hours) * 100,
            2
        )

    def classify_utilization(
        self,
        utilization,
        high_threshold=70,
        medium_threshold=40
    ):
        if utilization >= high_threshold:
            return "High"

        elif utilization >= medium_threshold:
            return "Medium"

        return "Low"

    def get_driver_utilization(
        self,
        driver_id,
        high_threshold=70,
        medium_threshold=40
    ):
        online_hours = self.calculate_online_hours(driver_id)
        busy_hours = self.calculate_busy_hours(driver_id)
        idle_hours = self.calculate_idle_hours(driver_id)
        utilization = self.calculate_utilization(driver_id)

        classification = self.classify_utilization(
            utilization,
            high_threshold,
            medium_threshold
        )

        return {
            "driver_id": driver_id,
            "online_hours": online_hours,
            "busy_hours": busy_hours,
            "idle_hours": idle_hours,
            "utilization": utilization,
            "classification": classification
        }