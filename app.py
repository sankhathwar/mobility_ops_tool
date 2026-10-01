from flask import Flask, render_template, request
import os
import pandas as pd

from services.validation_service import DataValidator
from services.zone_analyzer import ZoneAnalyzer
from services.data_loader import DataLoader
from services.driver_analyzer import DriverAnalyzer
from services.trip_analyzer import TripAnalyzer
from services.dashboard_analyzer import DashboardAnalyzer
from services.cancellation_analyzer import CancellationAnalyzer
from services.utilization_analyzer import UtilizationAnalyzer
from services.idle_time_analyzer import IdleTimeAnalyzer
from services.anomaly_detector import AnomalyDetector
from services.search_engine import SearchEngine
from models.zone import Zone
from services.insights_engine import InsightsEngine
from services.top_k_analyzer import TopKAnalyzer


app = Flask(__name__)


# =========================================================
# UPLOAD CONFIGURATION
# =========================================================

UPLOAD_FOLDER = "data/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# DATA LOADER
# =========================================================

loader = DataLoader()


# =========================================================
# LOAD DATASET
# =========================================================

def load_dataset(
    drivers_path,
    trips_path,
    activity_path
):
    global drivers
    global trips
    global activities

    global driver_analyzer
    global trip_analyzer
    global dashboard_analyzer
    global zone_analyzer
    global cancellation_analyzer
    global utilization_analyzer
    global idle_time_analyzer
    global anomaly_detector
    global search_engine
    global insights_engine

    # -----------------------------------------------------
    # Load data and create objects
    # -----------------------------------------------------

    drivers = loader.load_drivers(
        drivers_path
    )

    trips = loader.load_trips(
        trips_path
    )

    activities = loader.load_driver_activity(
        activity_path
    )

    # -----------------------------------------------------
    # Create analyzers
    # -----------------------------------------------------

    driver_analyzer = DriverAnalyzer(
        drivers,
        trips
    )

    trip_analyzer = TripAnalyzer(
        trips
    )

    dashboard_analyzer = DashboardAnalyzer(
        driver_analyzer,
        trip_analyzer
    )

    zone_analyzer = ZoneAnalyzer(
        trips
    )

    cancellation_analyzer = CancellationAnalyzer(
        trips
    )

    utilization_analyzer = UtilizationAnalyzer(
        activities,
        trips
    )

    idle_time_analyzer = IdleTimeAnalyzer(
        trips
    )

    anomaly_detector = AnomalyDetector(
        drivers,
        trips,
        utilization_analyzer
    )

    # -----------------------------------------------------
    # Create Zone objects
    # -----------------------------------------------------

    zone_names = sorted(
        set(
            trip.pickup_zone
            for trip in trips
            if trip.pickup_zone
        )
    )

    zones = [
        Zone(
            zone_id=zone_name,
            city="Bangalore"
        )
        for zone_name in zone_names
    ]

    # -----------------------------------------------------
    # Create search indexes
    # -----------------------------------------------------

    search_engine = SearchEngine(
        drivers,
        trips,
        zones
    )

    # -----------------------------------------------------
    # Create insights engine
    # -----------------------------------------------------

    insights_engine = InsightsEngine(
    zone_analyzer,
    cancellation_analyzer,
    anomaly_detector,
    utilization_analyzer,
    trips,
    drivers
    )


# =========================================================
# INITIAL DATASET
# =========================================================

load_dataset(
    "data/Drivers.csv",
    "data/Trips.csv",
    "data/Driver_activity.csv"
)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# DATA UPLOAD + VALIDATION
# =========================================================

@app.route(
    "/upload",
    methods=["GET", "POST"]
)
def upload():

    errors = []
    success = False

    if request.method == "POST":

        # -------------------------------------------------
        # Get uploaded files
        # -------------------------------------------------

        drivers_file = request.files.get(
            "drivers_file"
        )

        trips_file = request.files.get(
            "trips_file"
        )

        activity_file = request.files.get(
            "activity_file"
        )

        # -------------------------------------------------
        # Check all files are provided
        # -------------------------------------------------

        if (
            not drivers_file
            or not trips_file
            or not activity_file
        ):

            errors.append({
                "type": "Upload Error",
                "message": (
                    "Please upload all three CSV files."
                )
            })

        else:

            try:

                # -----------------------------------------
                # Read CSV files
                # -----------------------------------------

                drivers_df = pd.read_csv(
                    drivers_file
                )

                trips_df = pd.read_csv(
                    trips_file
                )

                activity_df = pd.read_csv(
                    activity_file
                )

                # -----------------------------------------
                # Convert trip timestamps
                # -----------------------------------------

                datetime_columns = [
                    "request_time",
                    "pickup_time",
                    "drop_time"
                ]

                for column in datetime_columns:

                    if column in trips_df.columns:

                        trips_df[column] = pd.to_datetime(
                            trips_df[column],
                            errors="coerce"
                        )

                # -----------------------------------------
                # Convert activity timestamps
                # -----------------------------------------

                if "timestamp" in activity_df.columns:

                    activity_df["timestamp"] = pd.to_datetime(
                        activity_df["timestamp"],
                        errors="coerce"
                    )

                # -----------------------------------------
                # Validate data
                # -----------------------------------------

                validator = DataValidator()

                errors = validator.validate_all(
                    drivers_df,
                    trips_df,
                    activity_df
                )

                # -----------------------------------------
                # If validation succeeds
                # -----------------------------------------

                if not errors:

                    drivers_path = os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        "Drivers.csv"
                    )

                    trips_path = os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        "Trips.csv"
                    )

                    activity_path = os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        "Driver_activity.csv"
                    )

                    # Save validated files
                    drivers_df.to_csv(
                        drivers_path,
                        index=False
                    )

                    trips_df.to_csv(
                        trips_path,
                        index=False
                    )

                    activity_df.to_csv(
                        activity_path,
                        index=False
                    )

                    # -------------------------------------
                    # IMPORTANT:
                    # Reload the entire analytics engine
                    # using the newly uploaded dataset.
                    # -------------------------------------

                    load_dataset(
                        drivers_path,
                        trips_path,
                        activity_path
                    )

                    success = True

            except Exception as e:

                errors.append({
                    "type": "Upload Error",
                    "message": str(e)
                })

    return render_template(
        "upload.html",
        errors=errors,
        success=success
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    metrics = (
        dashboard_analyzer
        .get_kpis()
    )

    return render_template(
        "dashboard.html",
        metrics=metrics
    )


# =========================================================
# DRIVER ANALYTICS
# =========================================================

@app.route("/drivers")
def drivers_page():

    selected_driver_id = request.args.get(
        "driver_id"
    )

    selected_driver = None
    selected_metrics = None

    if selected_driver_id:

        selected_driver = (
            driver_analyzer
            .get_driver(
                selected_driver_id
            )
        )

        if selected_driver:

            selected_metrics = (
                driver_analyzer
                .get_driver_performance(
                    selected_driver_id
                )
            )

    top_drivers = (
        driver_analyzer
        .get_top_drivers_by_completed_trips(5)
    )

    highest_revenue = (
        driver_analyzer
        .get_highest_revenue_drivers(5)
    )

    lowest_cancellation = (
        driver_analyzer
        .get_lowest_cancellation_drivers(5)
    )

    attention_drivers = (
        driver_analyzer
        .get_drivers_requiring_attention()
    )
    highest_utilization = (
        driver_analyzer
        .get_highest_utilization_drivers(
            utilization_analyzer,
            5
        )
    )

    return render_template(
        "driver.html",
        drivers=drivers,
        selected_driver=selected_driver,
        selected_metrics=selected_metrics,
        top_drivers=top_drivers,
        highest_revenue=highest_revenue,
        lowest_cancellation=lowest_cancellation,
        highest_utilization=highest_utilization,
        attention_drivers=attention_drivers
    )


# =========================================================
# ZONE ANALYTICS
# =========================================================

@app.route("/zones")
def zones_page():

    selected_city = request.args.get("city")
    selected_zone = request.args.get("zone")

    cities = zone_analyzer.get_cities()

    if selected_city and selected_city not in cities:
        selected_city = None

    zones = zone_analyzer.get_zones(selected_city)

    zone_metrics = None

    if selected_zone and selected_zone in zones:
        zone_metrics = zone_analyzer.get_zone_metrics(
            selected_zone,
            selected_city
        )

    return render_template(
        "zone.html",
        cities=cities,
        zones=zones,
        selected_city=selected_city,
        selected_zone=selected_zone,
        zone_metrics=zone_metrics
    )


# =========================================================
# CANCELLATION ANALYTICS
# =========================================================

@app.route("/cancellations")
def cancellations_page():

    summary = (
        cancellation_analyzer
        .get_cancellation_summary()
    )

    return render_template(
        "cancellations.html",
        summary=summary
    )


# =========================================================
# DRIVER UTILIZATION + IDLE TIME
# =========================================================

@app.route("/utilization")
def utilization_page():

    selected_driver_id = request.args.get(
        "driver_id"
    )

    threshold = request.args.get(
        "threshold",
        default=60,
        type=int
    )

    utilization_data = None
    idle_data = None

    if selected_driver_id:

        utilization_data = (
            utilization_analyzer
            .get_driver_utilization(
                selected_driver_id
            )
        )

        idle_data = (
            idle_time_analyzer
            .get_driver_idle_summary(
                selected_driver_id,
                threshold_minutes=threshold
            )
        )

    driver_ids = sorted(
        set(
            driver.driver_id
            for driver in drivers
        )
    )

    return render_template(
        "utilization.html",
        driver_ids=driver_ids,
        selected_driver_id=selected_driver_id,
        threshold=threshold,
        utilization_data=utilization_data,
        idle_data=idle_data
    )


# =========================================================
# ANOMALY DETECTION
# =========================================================

@app.route("/anomalies")
def anomalies_page():

    anomalies = (
        anomaly_detector
        .get_all_anomalies()
    )

    return render_template(
        "anomalies.html",
        anomalies=anomalies
    )


# =========================================================
# SEARCH ENGINE
# =========================================================

@app.route("/search")
def search_page():

    search_type = request.args.get(
        "type"
    )

    search_id = request.args.get(
        "id"
    )

    result = None

    if search_type and search_id:

        if search_type == "driver":

            result = (
                search_engine
                .search_driver(
                    search_id
                )
            )

        elif search_type == "trip":

            result = (
                search_engine
                .search_trip(
                    search_id
                )
            )

        elif search_type == "zone":

            result = (
                search_engine
                .search_zone(
                    search_id
                )
            )

    return render_template(
        "search.html",
        search_type=search_type,
        search_id=search_id,
        result=result
    )


# =========================================================
# INSIGHTS ENGINE
# =========================================================

@app.route("/insights")
def insights_page():

    insights = (
        insights_engine
        .generate_insights()
    )

    return render_template(
        "insights.html",
        insights=insights
    )

# =========================================================
# TOP-K ANALYSIS
# =========================================================

# =========================================================
# TOP-K ANALYSIS
# =========================================================

@app.route("/top-k")
def top_k_page():

    k = request.args.get(
        "k",
        default=5,
        type=int
    )

    # Prevent invalid K values
    if k <= 0:
        k = 5

    # -----------------------------------------------------
    # Top K drivers by completed trips
    # -----------------------------------------------------

    top_driver_objects = TopKAnalyzer.top_k(
        drivers,
        lambda driver: (
            driver_analyzer
            .get_driver_performance(
                driver.driver_id
            )["completed_trips"]
        ),
        k
    )

    top_drivers = []

    for driver in top_driver_objects:

        metrics = (
            driver_analyzer
            .get_driver_performance(
                driver.driver_id
            )
        )

        top_drivers.append({
            "driver": driver,
            "completed_trips": metrics["completed_trips"]
        })


    # -----------------------------------------------------
    # Top K drivers by revenue
    # -----------------------------------------------------

    revenue_driver_objects = TopKAnalyzer.top_k(
        drivers,
        lambda driver: (
            driver_analyzer
            .get_driver_performance(
                driver.driver_id
            )["revenue"]
        ),
        k
    )

    highest_revenue = []

    for driver in revenue_driver_objects:

        metrics = (
            driver_analyzer
            .get_driver_performance(
                driver.driver_id
            )
        )

        highest_revenue.append({
            "driver": driver,
            "revenue": metrics["revenue"]
        })


    # -----------------------------------------------------
    # Top K zones by demand
    # -----------------------------------------------------

    zones = (
        zone_analyzer
        .get_zones()
    )

    top_zone_objects = TopKAnalyzer.top_k(
        zones,
        lambda zone: (
            zone_analyzer
            .get_total_requests(zone)
        ),
        k
    )

    top_zones_by_demand = []

    for zone in top_zone_objects:

        top_zones_by_demand.append({
            "zone": zone,
            "requests": (
                zone_analyzer
                .get_total_requests(zone)
            )
        })


    # -----------------------------------------------------
    # Top K zones by cancellations
    # -----------------------------------------------------

    cancellation_zone_objects = TopKAnalyzer.top_k(
        zones,
        lambda zone: (
            zone_analyzer
            .get_cancelled_trips(zone)
        ),
        k
    )

    top_zones_by_cancellations = []

    for zone in cancellation_zone_objects:

        top_zones_by_cancellations.append({
            "zone": zone,
            "cancellations": (
                zone_analyzer
                .get_cancelled_trips(zone)
            )
        })


    # -----------------------------------------------------
    # Top K riders by trip count
    # -----------------------------------------------------

    rider_counts = {}

    for trip in trips:

        rider_counts[trip.rider_id] = (
            rider_counts.get(
                trip.rider_id,
                0
            ) + 1
        )

    top_riders = TopKAnalyzer.top_k(
        list(rider_counts.items()),
        lambda item: item[1],
        k
    )


    # -----------------------------------------------------
    # Render page
    # -----------------------------------------------------

    return render_template(
        "top_k.html",
        k=k,
        top_drivers=top_drivers,
        highest_revenue=highest_revenue,
        top_zones_by_demand=top_zones_by_demand,
        top_zones_by_cancellations=top_zones_by_cancellations,
        top_riders=top_riders
    )

    return render_template(
        "top_k.html",
        k=k,
        top_drivers=top_drivers,
        highest_revenue=highest_revenue,
        top_zones_by_demand=top_zones_by_demand,
        top_zones_by_cancellations=top_zones_by_cancellations,
        top_riders=top_riders
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )