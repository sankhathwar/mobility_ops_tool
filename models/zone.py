class Zone:
    def __init__(self, zone_id, city):
        self.zone_id = zone_id
        self.city = city

    def get_profile(self):
        return {
            "zone_id": self.zone_id,
            "city": self.city
        }

    def __repr__(self):
        return f"Zone({self.zone_id}, {self.city})"