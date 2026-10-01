class ZoneAnalyzer:

    def __init__(self, trips):
        self.trips = trips

    def get_cities(self):
        cities = set()

        for trip in self.trips:
            if trip.city:
                cities.add(trip.city)

        return sorted(cities)

    def get_zones(self, city=None):
        zones = set()

        for trip in self.trips:

            if not trip.pickup_zone:
                continue

            if city and trip.city != city:
                continue

            zones.add(trip.pickup_zone)

        return sorted(zones)

    def get_zone_trips(self, zone, city=None):
        return [
            trip
            for trip in self.trips
            if trip.pickup_zone == zone
            and (city is None or trip.city == city)
        ]

    def get_total_requests(self, zone, city=None):
        return len(self.get_zone_trips(zone, city))

    def get_completed_trips(self, zone, city=None):
        return sum(
            1
            for trip in self.get_zone_trips(zone, city)
            if trip.is_completed()
        )

    def get_cancelled_trips(self, zone, city=None):
        return sum(
            1
            for trip in self.get_zone_trips(zone, city)
            if trip.status.lower() == "cancelled"
        )

    def get_completion_rate(self, zone, city=None):
        total = self.get_total_requests(zone, city)

        if total == 0:
            return 0

        return round(
            (self.get_completed_trips(zone, city) / total) * 100,
            2
        )

    def get_cancellation_rate(self, zone, city=None):
        total = self.get_total_requests(zone, city)

        if total == 0:
            return 0

        return round(
            (self.get_cancelled_trips(zone, city) / total) * 100,
            2
        )

    def get_revenue(self, zone, city=None):
        return sum(
            trip.fare
            for trip in self.get_zone_trips(zone, city)
            if trip.is_completed()
            and trip.fare is not None
        )

    def get_average_fare(self, zone, city=None):
        trips = self.get_zone_trips(zone, city)

        valid_fares = [
            trip.fare
            for trip in trips
            if trip.fare is not None
        ]

        if not valid_fares:
            return 0

        return round(
            sum(valid_fares) / len(valid_fares),
            2
        )

    def get_demand_distribution(self, zone, city=None):

        distribution = {
            "06-09": 0,
            "09-12": 0,
            "12-15": 0,
            "15-18": 0,
            "18-21": 0,
            "21-00": 0
        }

        for trip in self.get_zone_trips(zone, city):

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

        return distribution

    def get_zone_metrics(self, zone, city=None):

        return {
            "zone": zone,
            "city": city,
            "total_requests": self.get_total_requests(zone, city),
            "completed_trips": self.get_completed_trips(zone, city),
            "cancelled_trips": self.get_cancelled_trips(zone, city),
            "completion_rate": self.get_completion_rate(zone, city),
            "cancellation_rate": self.get_cancellation_rate(zone, city),
            "revenue": self.get_revenue(zone, city),
            "average_fare": self.get_average_fare(zone, city),
            "demand_distribution": self.get_demand_distribution(
                zone,
                city
            )
        }