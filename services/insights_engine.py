class InsightsEngine:

    def __init__(
        self,
        zone_analyzer,
        cancellation_analyzer,
        anomaly_detector,
        utilization_analyzer,
        trips,
        drivers
    ):
        self.zone_analyzer = zone_analyzer
        self.cancellation_analyzer = cancellation_analyzer
        self.anomaly_detector = anomaly_detector
        self.utilization_analyzer = utilization_analyzer
        self.trips = trips
        self.drivers = drivers

    def get_highest_cancellation_zone(self):
        zones = self.zone_analyzer.get_zones()

        if not zones:
            return None

        zone_rates = {
            zone: self.zone_analyzer.get_cancellation_rate(zone)
            for zone in zones
        }

        return max(
            zone_rates,
            key=zone_rates.get
        )

    def get_peak_demand_period(self):
        distribution = {
            "06-09": 0,
            "09-12": 0,
            "12-15": 0,
            "15-18": 0,
            "18-21": 0,
            "21-00": 0
        }

        for trip in self.trips:

            if trip.request_time is None:
                continue

            hour = trip.request_time.hour

            if 6 <= hour < 9:
                distribution["06-09"] += 1

            elif 9 <= hour < 12:
                distribution["09-12"] += 1

            elif 12 <= hour < 15:
                distribution["12-15"] += 1

            elif 15 <= hour < 18:
                distribution["15-18"] += 1

            elif 18 <= hour < 21:
                distribution["18-21"] += 1

            elif 21 <= hour < 24:
                distribution["21-00"] += 1

        return max(
            distribution,
            key=distribution.get
        )

    def get_low_utilization_count(self, threshold=20):
        count = 0

        for driver in self.drivers:

            utilization = (
                self.utilization_analyzer
                .calculate_utilization(driver.driver_id)
            )

            if utilization < threshold:
                count += 1

        return count

    def get_largest_cancellation_category(self):
        cancellations = (
            self.cancellation_analyzer
            .get_cancellations_by_reason()
        )

        if not cancellations:
            return None

        return max(
            cancellations,
            key=cancellations.get
        )

    def get_anomaly_count(self):
        anomalies = self.anomaly_detector.get_all_anomalies()

        return sum(
            len(results)
            for results in anomalies.values()
        )

    def generate_insights(self):
        return {
            "highest_cancellation_zone":
                self.get_highest_cancellation_zone(),

            "peak_demand_period":
                self.get_peak_demand_period(),

            "low_utilization_count":
                self.get_low_utilization_count(),

            "largest_cancellation_category":
                self.get_largest_cancellation_category(),

            "anomaly_count":
                self.get_anomaly_count()
        }