import pandas as pd


class DataValidator:

    REQUIRED_COLUMNS = {

        "drivers": [
            "Driver_id",
            "driver_name",
            "city",
            "vehicle_type",
            "rating",
            "status"
        ],

        "trips": [
            "Trip_id",
            "driver_id",
            "rider_id",
            "city",
            "pickup_zone",
            "drop_zone",
            "request_time",
            "pickup_time",
            "drop_time",
            "distance_km",
            "fare",
            "status",
            "cancellation_reason"
        ],

        "activity": [
            "driver_id",
            "timestamp",
            "status"
        ]
    }


    def __init__(self):

        self.errors = []


    # =====================================================
    # REQUIRED COLUMNS
    # =====================================================

    def validate_required_columns(
        self,
        df,
        dataset_name
    ):

        required_columns = self.REQUIRED_COLUMNS[
            dataset_name
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:

            self.errors.append({
                "type": "Missing Columns",
                "dataset": dataset_name,
                "message": (
                    f"Missing required columns: "
                    f"{', '.join(missing_columns)}"
                )
            })

        return len(missing_columns) == 0


    # =====================================================
    # MISSING VALUES
    # =====================================================

    def validate_missing_values(
        self,
        df,
        dataset_name
    ):

        # -------------------------------------------------
        # Drivers and activity
        # -------------------------------------------------

        if dataset_name in [
            "drivers",
            "activity"
        ]:

            missing_counts = df.isnull().sum()

            for column, count in missing_counts.items():

                if count > 0:

                    self.errors.append({
                        "type": "Missing Values",
                        "dataset": dataset_name,
                        "column": column,
                        "count": int(count),
                        "message": (
                            f"{count} missing values found "
                            f"in {column}"
                        )
                    })

            return


        # -------------------------------------------------
        # Trips
        # -------------------------------------------------

        if dataset_name == "trips":

            # Fields required for every trip
            required_trip_columns = [

                "Trip_id",
                "driver_id",
                "rider_id",
                "city",
                "pickup_zone",
                "drop_zone",
                "request_time",
                "distance_km",
                "fare",
                "status"

            ]

            for column in required_trip_columns:

                count = df[column].isnull().sum()

                if count > 0:

                    self.errors.append({
                        "type": "Missing Values",
                        "dataset": "trips",
                        "column": column,
                        "count": int(count),
                        "message": (
                            f"{count} missing values found "
                            f"in {column}"
                        )
                    })


            # ---------------------------------------------
            # Completed trips
            # ---------------------------------------------

            completed_trips = df[
                df["status"]
                .astype(str)
                .str.lower()
                == "completed"
            ]

            for column in [
                "pickup_time",
                "drop_time"
            ]:

                count = (
                    completed_trips[column]
                    .isnull()
                    .sum()
                )

                if count > 0:

                    self.errors.append({
                        "type": "Missing Values",
                        "dataset": "trips",
                        "column": column,
                        "count": int(count),
                        "message": (
                            f"{count} completed trips have "
                            f"missing {column}"
                        )
                    })


            # ---------------------------------------------
            # Cancelled trips
            # ---------------------------------------------

            cancelled_trips = df[
                df["status"]
                .astype(str)
                .str.lower()
                == "cancelled"
            ]

            count = (
                cancelled_trips[
                    "cancellation_reason"
                ]
                .isnull()
                .sum()
            )

            if count > 0:

                self.errors.append({
                    "type": "Missing Values",
                    "dataset": "trips",
                    "column": "cancellation_reason",
                    "count": int(count),
                    "message": (
                        f"{count} cancelled trips have "
                        f"missing cancellation_reason"
                    )
                })


    # =====================================================
    # DRIVER ID VALIDATION
    # =====================================================

    def validate_driver_ids(
        self,
        drivers_df,
        trips_df,
        activity_df
    ):

        valid_driver_ids = set(
            drivers_df[
                "Driver_id"
            ].dropna()
        )


        # -------------------------------------------------
        # Trip driver IDs
        # -------------------------------------------------

        trip_driver_ids = set(
            trips_df[
                "driver_id"
            ].dropna()
        )

        unknown_trip_drivers = (
            trip_driver_ids
            - valid_driver_ids
        )

        for driver_id in unknown_trip_drivers:

            count = (
                trips_df["driver_id"]
                == driver_id
            ).sum()

            self.errors.append({
                "type": "Invalid Driver ID",
                "dataset": "trips",
                "id": driver_id,
                "count": int(count),
                "message": (
                    f"{count} trips reference "
                    f"unknown driver ID {driver_id}"
                )
            })


        # -------------------------------------------------
        # Activity driver IDs
        # -------------------------------------------------

        activity_driver_ids = set(
            activity_df[
                "driver_id"
            ].dropna()
        )

        unknown_activity_drivers = (
            activity_driver_ids
            - valid_driver_ids
        )

        for driver_id in unknown_activity_drivers:

            count = (
                activity_df["driver_id"]
                == driver_id
            ).sum()

            self.errors.append({
                "type": "Invalid Driver ID",
                "dataset": "activity",
                "id": driver_id,
                "count": int(count),
                "message": (
                    f"{count} activity records reference "
                    f"unknown driver ID {driver_id}"
                )
            })


    # =====================================================
    # TRIP ID VALIDATION
    # =====================================================

    def validate_trip_ids(
        self,
        trips_df
    ):

        duplicate_ids = (
            trips_df[
                trips_df[
                    "Trip_id"
                ].duplicated(
                    keep=False
                )
            ]["Trip_id"]
            .unique()
        )

        for trip_id in duplicate_ids:

            count = (
                trips_df["Trip_id"]
                == trip_id
            ).sum()

            self.errors.append({
                "type": "Invalid Trip ID",
                "dataset": "trips",
                "id": trip_id,
                "count": int(count),
                "message": (
                    f"Trip ID {trip_id} appears "
                    f"{count} times"
                )
            })


    # =====================================================
    # TIMESTAMP VALIDATION
    # =====================================================

    def validate_timestamps(
        self,
        trips_df,
        activity_df
    ):

        # -------------------------------------------------
        # Request time
        # Required for every trip
        # -------------------------------------------------

        invalid_request_time = (
            trips_df[
                "request_time"
            ]
            .isna()
            .sum()
        )

        if invalid_request_time > 0:

            self.errors.append({
                "type": "Invalid Timestamp",
                "dataset": "trips",
                "column": "request_time",
                "count": int(
                    invalid_request_time
                ),
                "message": (
                    f"{invalid_request_time} trips contain "
                    f"missing or invalid request_time"
                )
            })


        # -------------------------------------------------
        # Completed trips
        # -------------------------------------------------

        completed_trips = trips_df[
            trips_df["status"]
            .astype(str)
            .str.lower()
            == "completed"
        ]

        for column in [
            "pickup_time",
            "drop_time"
        ]:

            invalid_count = (
                completed_trips[column]
                .isna()
                .sum()
            )

            if invalid_count > 0:

                self.errors.append({
                    "type": "Invalid Timestamp",
                    "dataset": "trips",
                    "column": column,
                    "count": int(
                        invalid_count
                    ),
                    "message": (
                        f"{invalid_count} completed trips "
                        f"contain missing or invalid "
                        f"{column}"
                    )
                })


        # -------------------------------------------------
        # Driver activity timestamps
        # -------------------------------------------------

        invalid_activity_timestamps = (
            activity_df[
                "timestamp"
            ]
            .isna()
            .sum()
        )

        if invalid_activity_timestamps > 0:

            self.errors.append({
                "type": "Invalid Timestamp",
                "dataset": "activity",
                "column": "timestamp",
                "count": int(
                    invalid_activity_timestamps
                ),
                "message": (
                    f"{invalid_activity_timestamps} activity "
                    f"records contain invalid timestamps"
                )
            })


    # =====================================================
    # NEGATIVE FARE
    # =====================================================

    def validate_negative_fares(
        self,
        trips_df
    ):

        negative_fares = trips_df[
            trips_df["fare"] < 0
        ]

        if not negative_fares.empty:

            self.errors.append({
                "type": "Negative Fare",
                "dataset": "trips",
                "count": len(
                    negative_fares
                ),
                "message": (
                    f"{len(negative_fares)} trips "
                    f"contain negative fare"
                )
            })


    # =====================================================
    # TRIP DURATION
    # =====================================================

    def validate_trip_durations(
        self,
        trips_df
    ):

        invalid_duration_count = 0

        for _, row in trips_df.iterrows():

            pickup = row["pickup_time"]
            drop = row["drop_time"]

            # Cancelled trips can have missing timestamps
            if (
                pd.notna(pickup)
                and pd.notna(drop)
            ):

                if drop < pickup:

                    invalid_duration_count += 1


        if invalid_duration_count > 0:

            self.errors.append({
                "type": "Invalid Trip Duration",
                "dataset": "trips",
                "count": (
                    invalid_duration_count
                ),
                "message": (
                    f"{invalid_duration_count} trips have "
                    f"drop time earlier than pickup time"
                )
            })


    # =====================================================
    # DISTANCE VALIDATION
    # =====================================================

    def validate_distances(
        self,
        trips_df
    ):

        invalid_distance_count = (
            trips_df[
                "distance_km"
            ] < 0
        ).sum()

        if invalid_distance_count > 0:

            self.errors.append({
                "type": "Invalid Distance",
                "dataset": "trips",
                "count": int(
                    invalid_distance_count
                ),
                "message": (
                    f"{invalid_distance_count} trips contain "
                    f"negative distance"
                )
            })


    # =====================================================
    # COMPLETE VALIDATION
    # =====================================================

    def validate_all(
        self,
        drivers_df,
        trips_df,
        activity_df
    ):

        # Reset previous errors
        self.errors = []


        # -------------------------------------------------
        # Required columns
        # -------------------------------------------------

        drivers_valid = (
            self.validate_required_columns(
                drivers_df,
                "drivers"
            )
        )

        trips_valid = (
            self.validate_required_columns(
                trips_df,
                "trips"
            )
        )

        activity_valid = (
            self.validate_required_columns(
                activity_df,
                "activity"
            )
        )


        # -------------------------------------------------
        # Stop if required columns are missing
        # -------------------------------------------------

        if (
            not drivers_valid
            or not trips_valid
            or not activity_valid
        ):

            return self.errors


        # -------------------------------------------------
        # Missing values
        # -------------------------------------------------

        self.validate_missing_values(
            drivers_df,
            "drivers"
        )

        self.validate_missing_values(
            trips_df,
            "trips"
        )

        self.validate_missing_values(
            activity_df,
            "activity"
        )


        # -------------------------------------------------
        # IDs
        # -------------------------------------------------

        self.validate_driver_ids(
            drivers_df,
            trips_df,
            activity_df
        )

        self.validate_trip_ids(
            trips_df
        )


        # -------------------------------------------------
        # Timestamps
        # -------------------------------------------------

        self.validate_timestamps(
            trips_df,
            activity_df
        )


        # -------------------------------------------------
        # Fare
        # -------------------------------------------------

        self.validate_negative_fares(
            trips_df
        )


        # -------------------------------------------------
        # Duration
        # -------------------------------------------------

        self.validate_trip_durations(
            trips_df
        )


        # -------------------------------------------------
        # Distance
        # -------------------------------------------------

        self.validate_distances(
            trips_df
        )


        return self.errors