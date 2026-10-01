class DriverActivity:
    def __init__(self, driver_id, timestamp, status):
        self.driver_id = driver_id
        self.timestamp = timestamp
        self.status = status

    def is_online(self):
        return self.status.lower() == "online"

    def is_offline(self):
        return self.status.lower() == "offline"

    def __repr__(self):
        return f"DriverActivity({self.driver_id}, {self.timestamp}, {self.status})"