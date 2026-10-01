class SearchEngine:

    def __init__(self, drivers, trips, zones):
        self.driver_index = {
            driver.driver_id: driver
            for driver in drivers
        }

        self.trip_index = {
            trip.trip_id: trip
            for trip in trips
        }

        self.zone_index = {
            zone.zone_id: zone
            for zone in zones
        }

    def search_driver(self, driver_id):
        return self.driver_index.get(driver_id)

    def search_trip(self, trip_id):
        return self.trip_index.get(trip_id)

    def search_zone(self, zone_id):
        return self.zone_index.get(zone_id)