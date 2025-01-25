from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
from etl_pipeline import run_etl
from datetime import datetime
from geopy.distance import geodesic

app = Flask(__name__)

# File paths
GPS_DATA_PATH = "data/gps_data.json"
ROUTE_SCHEDULE_PATH = "data/route_schedule.csv"
OUTPUT_FILE_PATH = "data/output.parquet"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract():
    # Load the full input data
    gps_data = pd.read_json(GPS_DATA_PATH)
    route_schedule = pd.read_csv(ROUTE_SCHEDULE_PATH)

    # Convert timestamps to UTC in both datasets
    # gps_data['current_time'] = pd.to_datetime(gps_data['current_time']).dt.tz_localize('UTC')
    # route_schedule['scheduled_time'] = pd.to_datetime(route_schedule['scheduled_time']).dt.tz_localize('UTC')

    return jsonify({
        "gps_data": gps_data.to_dict(orient="records"),
        "route_schedule": route_schedule.to_dict(orient="records")
    })

@app.route("/transform", methods=["POST"])
def transform():
    try:
        run_etl(GPS_DATA_PATH, ROUTE_SCHEDULE_PATH, OUTPUT_FILE_PATH)
        return jsonify({"status": "success", "message": "Transformation completed."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/load", methods=["POST"])
def load():
    # Load output data
    output_data = pd.read_parquet(OUTPUT_FILE_PATH)

    # Return the output data in the correct column order
    return jsonify({"output_data": output_data.to_dict(orient="records")})

if __name__ == "__main__":
    app.run(debug=True)
