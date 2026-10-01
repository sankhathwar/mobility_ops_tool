from services.top_k_analyzer import TopKAnalyzer
class DriverAnalyzer:

    def __init__(self, drivers, trips):
        self.drivers = drivers
        self.trips = trips

        # Hash-map index:
        # Driver ID -> Driver object
        self.driver_index = {
            driver.driver_id: driver
            for driver in drivers
        }

    def get_total_drivers(self):
        return len(self.drivers)

    def get_active_drivers(self):
        return sum(
            1
            for driver in self.drivers
            if driver.is_active()
        )

    def get_driver(self, driver_id):
        return self.driver_index.get(driver_id)

    def get_driver_trips(self, driver_id):
        return [
            trip
            for trip in self.trips
            if trip.driver_id == driver_id
        ]

    def get_driver_performance(self, driver_id):

        driver = self.get_driver(driver_id)

        if driver is None:
            return None

        driver_trips = self.get_driver_trips(driver_id)

        total_trips = len(driver_trips)

        completed_trips = sum(
            1
            for trip in driver_trips
            if trip.is_completed()
        )

        cancelled_trips = sum(
            1
            for trip in driver_trips
            if trip.status.lower() == "cancelled"
        )

        completion_rate = (
            completed_trips / total_trips * 100
            if total_trips > 0
            else 0
        )

        cancellation_rate = (
            cancelled_trips / total_trips * 100
            if total_trips > 0
            else 0
        )

        revenue = sum(
            trip.fare
            for trip in driver_trips
            if trip.is_completed()
            and trip.fare is not None
            and trip.fare > 0
        )

        completed_fares = [
            trip.fare
            for trip in driver_trips
            if trip.is_completed()
            and trip.fare is not None
            and trip.fare >= 0
        ]

        average_fare = (
            sum(completed_fares) / len(completed_fares)
            if completed_fares
            else 0
        )

        completed_distances = [
            trip.distance_km
            for trip in driver_trips
            if trip.is_completed()
            and trip.distance_km is not None
            and trip.distance_km >= 0
        ]

        average_distance = (
            sum(completed_distances)
            / len(completed_distances)
            if completed_distances
            else 0
        )

        fare_per_km_values = [
            trip.calculate_fare_per_km()
            for trip in driver_trips
            if trip.is_completed()
            and trip.calculate_fare_per_km() is not None
        ]

        average_fare_per_km = (
            sum(fare_per_km_values)
            / len(fare_per_km_values)
            if fare_per_km_values
            else 0
        )

        return {
            "driver_id": driver.driver_id,
            "driver_name": driver.driver_name,
            "city": driver.city,
            "vehicle_type": driver.vehicle_type,
            "rating": driver.rating,
            "status": driver.status,
            "total_trips": total_trips,
            "completed_trips": completed_trips,
            "cancelled_trips": cancelled_trips,
            "completion_rate": completion_rate,
            "cancellation_rate": cancellation_rate,
            "revenue": revenue,
            "average_fare": average_fare,
            "average_distance": average_distance,
            "average_fare_per_km": average_fare_per_km
        }

    def get_all_driver_performance(self):

        performance = []

        for driver in self.drivers:

            result = self.get_driver_performance(
                driver.driver_id
            )

            performance.append(result)

        return performance

    def get_top_drivers_by_completed_trips(self, k=5):
        performance = self.get_all_driver_performance()
        
        return TopKAnalyzer.top_k(
        performance,
        metric_function=lambda x: x["completed_trips"],
        k=k
    )

    def get_lowest_cancellation_drivers(self, k=5):

        performance = self.get_all_driver_performance()

        return sorted(
            performance,
            key=lambda x: x["cancellation_rate"]
        )[:k]

    def get_highest_revenue_drivers(self, k=5):

        performance = self.get_all_driver_performance()

        return TopKAnalyzer.top_k(
        performance,
        metric_function=lambda x: x["revenue"],
        k=k
    )

    def get_drivers_requiring_attention(
        self,
        cancellation_threshold=30,
        rating_threshold=4.0
    ):

        performance = self.get_all_driver_performance()

        attention = []

        for driver in performance:

            issues = []

            if (
                driver["cancellation_rate"]
                > cancellation_threshold
            ):
                issues.append(
                    "High cancellation rate"
                )

            if driver["rating"] < rating_threshold:
                issues.append(
                    "Low rating"
                )

            if issues:
                driver["issues"] = issues
                attention.append(driver)

        return attention


    def get_highest_utilization_drivers(
        self,
        utilization_analyzer,
        k=5
    ):

        performance = []

        for driver in self.drivers:

            utilization = (
                utilization_analyzer
                .calculate_utilization(driver.driver_id)
            )

            performance.append({
                "driver_id": driver.driver_id,
                "driver_name": driver.driver_name,
                "utilization": utilization
            })

        return TopKAnalyzer.top_k(
            performance,
            metric_function=lambda x: x["utilization"],
            k=k
        )

    def get_driver_metrics(self):

        return {
            "total_drivers": self.get_total_drivers(),
            "active_drivers": self.get_active_drivers()
        }