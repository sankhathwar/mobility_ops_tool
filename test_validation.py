import pandas as pd

from services.validation_service import DataValidator


drivers_df = pd.read_csv(
    "data/Drivers.csv"
)

trips_df = pd.read_csv(
    "data/Trips.csv"
)

activity_df = pd.read_csv(
    "data/Driver_activity.csv"
)


# Convert timestamps
trips_df["request_time"] = pd.to_datetime(
    trips_df["request_time"],
    errors="coerce"
)

trips_df["pickup_time"] = pd.to_datetime(
    trips_df["pickup_time"],
    errors="coerce"
)

trips_df["drop_time"] = pd.to_datetime(
    trips_df["drop_time"],
    errors="coerce"
)

activity_df["timestamp"] = pd.to_datetime(
    activity_df["timestamp"],
    errors="coerce"
)


validator = DataValidator()

errors = validator.validate_all(
    drivers_df,
    trips_df,
    activity_df
)


print("\nDATA VALIDATION RESULTS")
print("-" * 50)

if not errors:

    print("No validation errors found.")

else:

    for error in errors:

        print(
            f"[{error['type']}] "
            f"{error['message']}"
        )