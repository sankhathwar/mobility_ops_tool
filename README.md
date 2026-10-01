# Mobility Marketplace Operations Intelligence Engine

A Python and Flask-based analytics application for analysing mobility marketplace operations.

The application allows an operations user to upload driver, trip, and driver-activity CSV files and interactively analyse driver performance, trip activity, zones, cancellations, utilisation, idle time, anomalies, search results, Top-K metrics, and operational insights.

## Features

### 1. Data Upload and Validation
The application accepts three CSV files:

- `Drivers.csv`
- `Trips.csv`
- `Driver_activity.csv`

Validation checks include:

- Required columns
- Missing values
- Invalid driver IDs
- Invalid timestamps
- Negative fares
- Negative distances
- Invalid trip durations
- Duplicate trip IDs
- Status-dependent trip fields

Invalid data is rejected and validation errors are displayed to the user.

### 2. Operations Dashboard

The dashboard dynamically calculates:

- Total Drivers
- Active Drivers
- Total Riders
- Total Trips
- Completed Trips
- Cancelled Trips
- Completion Rate
- Cancellation Rate
- Total Revenue
- Average Fare
- Average Trip Distance
- Average Trip Duration

All values are calculated from the currently loaded dataset.

### 3. Driver Analytics

Users can select an individual driver and view:

- Driver profile
- Total trips
- Completed trips
- Cancelled trips
- Completion rate
- Cancellation rate
- Revenue
- Average fare
- Average distance
- Average fare per kilometre

The application also provides:

- Top drivers by completed trips
- Highest revenue drivers
- Lowest cancellation drivers
- Highest utilisation drivers
- Drivers requiring operational attention

### 4. Top-K Analysis

Top-K analysis is implemented using a heap-based approach through Python's `heapq` module.

Available analyses include:

- Top K drivers by completed trips
- Top K drivers by revenue
- Top K zones by demand
- Top K zones by cancellations
- Top K riders by trip count

The value of K can be changed from the web interface.

### 5. Zone Analytics

Users can select a city and zone to analyse:

- Total requests
- Completed trips
- Cancelled trips
- Completion rate
- Cancellation rate
- Revenue
- Average fare

Demand is also distributed across:

- 06-09
- 09-12
- 12-15
- 15-18
- 18-21
- 21-00

### 6. Cancellation Intelligence

Cancellation analysis is available by:

- Cancellation reason
- Pickup zone
- Driver
- Time slot

The application also provides the total number of cancellations.

### 7. Driver Utilisation and Idle Time

For a selected driver, the application calculates:

- Online hours
- Busy hours
- Idle hours
- Utilisation percentage
- Utilisation classification

Utilisation is classified using configurable thresholds.

The application also calculates idle gaps between consecutive trips and allows the user to configure the idle-time threshold.

### 8. Anomaly Detection

The application identifies trip-level anomalies including:

- Negative fares
- Zero distance
- Invalid timestamps
- Extremely long trip duration
- Unknown drivers
- Unusual fares

Driver-level anomalies include:

- High cancellation rate
- Low utilisation
- High trip count
- Low rating

### 9. Search Engine

A dictionary/hash-map based index provides fast lookup for:

- Driver ID → Driver
- Trip ID → Trip
- Zone ID → Zone

### 10. Operational Insights

The Insights Engine dynamically generates:

- Highest cancellation zone
- Peak demand period
- Number of low-utilisation drivers
- Largest cancellation category
- Total anomaly count

These insights are calculated from the loaded dataset rather than hard-coded.

---

## Project Architecture

```text
mobility_operations_tool/
│
├── app.py
├── README.md
│
├── models/
│   ├── __init__.py
│   ├── driver.py
│   ├── trip.py
│   ├── zone.py
│   └── activity.py
│
├── services/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── validation_service.py
│   ├── dashboard_analyzer.py
│   ├── driver_analyzer.py
│   ├── trip_analyzer.py
│   ├── zone_analyzer.py
│   ├── utilization_analyzer.py
│   ├── idle_time_analyzer.py
│   ├── cancellation_analyzer.py
│   ├── top_k_analyzer.py
│   ├── search_engine.py
│   ├── insights_engine.py
│   └── anomaly_detector.py
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── constants.py
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── driver.html
│   ├── zone.html
│   ├── anomalies.html
│   ├── cancellations.html
│   ├── utilization.html
│   ├── search.html
│   ├── insights.html
│   ├── upload.html
│   └── top_k.html
│
├── static/
│   └── style.css
│
└── data/
    ├── Drivers.csv
    ├── Trips.csv
    └── Driver_activity.csv
```

## OOP Design

The application follows separation of responsibilities.

### Models

The model classes represent the core mobility entities:

- `Driver`
- `Trip`
- `Zone`
- `DriverActivity`

Examples of object behaviour include:

```python
driver.is_active()
driver.get_profile()

trip.is_completed()
trip.calculate_duration()
trip.calculate_fare_per_km()
```

### Services

The service classes contain data processing and analytical logic:

- `DataLoader`
- `DataValidator`
- `DashboardAnalyzer`
- `DriverAnalyzer`
- `TripAnalyzer`
- `ZoneAnalyzer`
- `UtilizationAnalyzer`
- `IdleTimeAnalyzer`
- `CancellationAnalyzer`
- `TopKAnalyzer`
- `SearchEngine`
- `InsightsEngine`
- `AnomalyDetector`

This keeps the Flask routes focused on application flow and presentation rather than putting all analytical logic inside `app.py`.

## Technology Stack

- Python 3
- Flask
- Pandas
- HTML
- CSS
- Jinja2
- Python `heapq`
- CSV data processing
- Object-Oriented Programming
- Data structures and algorithms

## Installation

### 1. Clone or copy the project

Open the project directory:

```bash
cd mobility_operations_tool
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

Install Flask and Pandas:

```bash
pip install flask pandas
```

## Running the Application

With the virtual environment activated:

```bash
python app.py
```

The Flask development server will start.

Open the application in a browser:

```text
http://127.0.0.1:5000
```

## Using the Application

### Step 1: Upload Data

Open:

```text
/upload
```

Upload:

- Drivers CSV
- Trips CSV
- Driver Activity CSV

The application validates the uploaded files before loading them.

### Step 2: Dashboard

Open the Dashboard to view the marketplace KPIs generated from the uploaded dataset.

### Step 3: Analyse Drivers

Use the Drivers page to select a driver and inspect individual performance.

### Step 4: Analyse Top-K Metrics

Use the Top-K page to select the required K value and analyse high-performing drivers, zones and riders.

### Step 5: Analyse Zones

Select a city and zone to view zone-level marketplace demand and performance.

### Step 6: Analyse Cancellations

Review cancellation patterns by reason, zone, driver and time.

### Step 7: Analyse Utilisation

Select a driver and configure an idle threshold to analyse utilisation and consecutive-trip idle periods.

### Step 8: Review Anomalies

Use the Anomalies page to identify unusual trips and driver behaviour.

### Step 9: Search

Search for a Driver ID, Trip ID or Zone ID using the indexed search engine.

### Step 10: Review Insights

The Insights page provides dynamically generated operational observations based on the loaded dataset.

## Sample Dataset

The `data/` directory contains sample CSV files that can be used to test the application.

The application is designed so that analytics are generated from the loaded data rather than being hard-coded.

## Data Flow

```text
CSV Upload / Sample Data
          |
          v
   Data Validation
          |
          v
    Object Creation
          |
          v
    Analytics Engine
          |
          +-------------------+
          |                   |
          v                   v
 Driver Analytics       Trip Analytics
          |                   |
          +---------+---------+
                    |
                    v
              Zone Analytics
                    |
                    v
          Cancellation Analysis
                    |
                    v
          Utilisation Analysis
                    |
                    v
           Anomaly Detection
                    |
                    v
            Insights Engine
                    |
                    v
          Interactive Flask UI
```

## DSA Concepts Used

The project demonstrates practical use of data structures and algorithms, including:

- Dictionaries/hash maps for indexed search and frequency counting
- Sets for unique cities and zones
- Lists for object collections and sequential trip processing
- Sorting for chronological trip analysis
- `heapq` priority queues for Top-K analysis
- Filtering and traversal for analytical calculations

## Validation and Edge Cases

The validation layer handles data-quality issues before data is loaded into the analytics engine.

Examples include:

- Missing required columns
- Missing required values
- Unknown driver IDs
- Invalid timestamps
- Negative fares
- Negative distances
- Invalid completed-trip durations
- Duplicate trip IDs

Trip validation is status-aware. Completed trips require pickup and drop timestamps, while cancelled trips require a cancellation reason.

## Notes

This project is intended as a mobility marketplace operations analytics tool and demonstrates:

- Python Object-Oriented Programming
- Data processing
- Analytical problem solving
- Data structures and algorithms
- Flask application development
- Operational analytics
- Dynamic insight generation