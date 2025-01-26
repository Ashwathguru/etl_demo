Here’s a detailed README file for your project:

---

# Live Transportation Delay Tracking Application

## Overview

This project is designed to track real-time transportation delays and estimate the approximate time of arrival (ETA) for buses based on live GPS data and scheduled route information. The application utilizes **PySpark** for processing large datasets and applying the necessary ETL (Extract, Transform, Load) operations to generate the results. The input data consists of live GPS data from buses and predefined route schedules, and at any given time, the application can provide the delay and ETA of the buses.

## Features

- **Real-time Delay Tracking:** Tracks the delay for buses by comparing their current GPS location with the scheduled stops.
- **Distance Calculation:** Computes the distance between the bus and its next scheduled stop using geodesic calculations.
- **ETA Calculation:** Estimates the approximate time of arrival (ETA) based on the current speed of the bus.
- **PySpark-based ETL Pipeline:** Utilizes PySpark for handling large datasets and performing efficient ETL processing.
- **Output in Parquet Format:** The results of the ETL pipeline are stored in a Parquet file for efficient querying and further analysis.

## Tech Stack

- **Backend Framework:** Flask (for building a simple web server to interact with the data)
- **ETL Processing:** PySpark (for handling data transformations and distance calculations)
- **Data Storage:** Parquet (for storing processed output in a highly efficient format)
- **Geospatial Calculations:** Geopy (for distance calculations between bus and scheduled stop)


## How It Works

### 1. **Extract:**
The application loads the GPS data from the `gps_data.json` file and the route schedule from the `route_schedule.csv` file. The data consists of:
- **GPS Data:** Live updates on bus locations, including bus ID, latitude, longitude, and timestamp.
- **Route Schedule:** Information about scheduled stops, including stop names, stop IDs, latitude, longitude, and scheduled times.

### 2. **Transform:**
The ETL pipeline performs several key transformations:
- **Distance Calculation:** Uses the `geopy` library to calculate the distance between the bus’s current GPS location and the scheduled stop.
- **Arrival Time Calculation:** If the bus is within 1 km of a stop, it is considered to have arrived, and the actual arrival time is recorded. Otherwise, an estimated arrival time is calculated based on the bus's current speed (default 20 km/h).
- **Time Adjustments:** Adjusts the scheduled time based on the calculated distance and bus speed.

### 3. **Load:**
The transformed data, which includes bus ID, route ID, stop ID, stop name, scheduled time, actual arrival time, approximate arrival time, and distance to the stop, is written to a Parquet file (`output.parquet`). This output is then accessible through the Flask app for querying.

### 4. **Web Interface:**
The Flask app provides an interface for:
- **Extracting Data:** Loads GPS and route schedule data and displays it.
- **Transforming Data:** Runs the ETL pipeline and outputs a success message.
- **Loading Data:** Loads the processed output data from the Parquet file and displays the results.

## Installation

### Prerequisites

- Python 3.7+
- Apache Spark (PySpark)
- Geopy
- Flask
- Pandas

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Live-Transportation-Delay-Tracking.git
cd Live-Transportation-Delay-Tracking
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Flask application

```bash
python app/__init__.py
```

The Flask app will start running on `http://127.0.0.1:5000`.

## Usage

### Extract Data

- Navigate to `http://127.0.0.1:5000/extract` to load the GPS and route schedule data.

### Transform Data

- Navigate to `http://127.0.0.1:5000/transform` to run the ETL pipeline, which will process the data and calculate delays and estimated arrival times.

### Load Processed Data

- Navigate to `http://127.0.0.1:5000/load` to view the processed data from the Parquet file, including the delay information and ETAs.

## Data Format

### GPS Data (`gps_data.json`)
This JSON file should contain live GPS updates for each bus. Example format:

```json
[
    {
        "bus_id": "1",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "current_time": "2025-01-26T12:00:00Z"
    },
    {
        "bus_id": "2",
        "latitude": 12.2958,
        "longitude": 76.6394,
        "current_time": "2025-01-26T12:05:00Z"
    }
]
```

### Route Schedule (`route_schedule.csv`)
This CSV file should contain scheduled stops for each route. Example format:

```csv
route_id,stop_id,stop_name,latitude,longitude,scheduled_time
1,1,"Stop 1",12.9716,77.5946,"2025-01-26T12:15:00Z"
1,2,"Stop 2",12.2958,76.6394,"2025-01-26T12:30:00Z"
```

## Potential Enhancements

- **Real-time Streaming:** Integrate Apache Kafka or other streaming technologies to handle live updates instead of batch processing.
- **Route Prediction:** Use machine learning models to predict future delays based on historical data.
- **Mobile App Integration:** Develop a mobile app for users to track bus delays in real-time.


---
