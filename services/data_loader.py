import pandas as pd

from models.driver import Driver
from models.trip import Trip
from models.activity import DriverActivity


class DataLoader:

    def load_drivers(self, file_path):
        df = pd.read_csv(file_path)

        drivers = []

        for _, row in df.iterrows():
            driver = Driver(
                driver_id=row["Driver_id"],
                driver_name=row["driver_name"],
                city=row["city"],
                vehicle_type=row["vehicle_type"],
                rating=row["rating"],
                status=row["status"]
            )

            drivers.append(driver)

        return drivers

    def load_trips(self, file_path):
        df = pd.read_csv(file_path)

        datetime_columns = [
            "request_time",
            "pickup_time",
            "drop_time"
        ]

        for column in datetime_columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

        trips = []

        for _, row in df.iterrows():
            trip = Trip(
                trip_id=row["Trip_id"],
                driver_id=row["driver_id"],
                rider_id=row["rider_id"],
                city=row["city"],
                pickup_zone=row["pickup_zone"],
                drop_zone=row["drop_zone"],
                request_time=row["request_time"],
                pickup_time=row["pickup_time"],
                drop_time=row["drop_time"],
                distance_km=row["distance_km"],
                fare=row["fare"],
                status=row["status"],
                cancellation_reason=row["cancellation_reason"]
            )

            trips.append(trip)

        return trips

    def load_driver_activity(self, file_path):
        df = pd.read_csv(file_path)

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            errors="coerce"
        )

        activities = []

        for _, row in df.iterrows():
            activity = DriverActivity(
                driver_id=row["driver_id"],
                timestamp=row["timestamp"],
                status=row["status"]
            )

            activities.append(activity)

        return activities