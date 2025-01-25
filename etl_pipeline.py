from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, from_unixtime, to_timestamp, unix_timestamp,udf,when,ceil
from geopy.distance import geodesic
from pyspark.sql.types import FloatType
import pandas as pd

# Speed of the bus in km/h
BUS_SPEED_KMH = 20

def run_etl(gps_data_path, route_schedule_path, output_file_path):
    # Initialize Spark session
    spark = SparkSession.builder.appName("ETL_Pipeline").getOrCreate()

   # Define the schema for GPS data
    # Load the GPS data (allow Spark to infer the schema)
    gps_data_path = "data/gps_data.json"
    gps_df = spark.read.option("multiline", "true").json(gps_data_path)
    
    # Load Route Schedule data
    routes_df = spark.read.csv(route_schedule_path, header=True, inferSchema=True) \
    .withColumnRenamed("latitude", "stop_latitude") \
    .withColumnRenamed("longitude", "stop_longitude") \
    .alias("routes")


    # Join GPS data with Route schedule data on bus_id
    gps_with_routes = gps_df.join(routes_df, on="bus_id")

    # Calculate the distance between the bus location and stop location
    gps_with_routes = gps_with_routes.withColumn(
        "distance_km",
        expr("""
            6371 * acos(
                cos(radians(latitude)) *
                cos(radians(stop_latitude)) *
                cos(radians(stop_longitude) - radians(longitude)) +
                sin(radians(latitude)) *
                sin(radians(routes.stop_latitude))
            )
        """)
    )

    gps_with_routes = gps_with_routes.select("bus_id","route_id","stop_id","stop_name","scheduled_time","current_time","distance_km")

    # Define the conditions
    df_with_times = gps_with_routes.withColumn(
        "actual_arrival_time", 
        when(gps_with_routes["distance_km"] <= 1, gps_with_routes["current_time"]).otherwise(None)
    ).withColumn(
        "time_taken_for_distance",
        ceil(3 * gps_with_routes["distance_km"]).cast("int")  # Rounding up the value
    )
    df_with_times = df_with_times.select("bus_id", "route_id", "stop_id", "stop_name", "scheduled_time", "current_time", "distance_km", "actual_arrival_time", "time_taken_for_distance")

    def add_minutes_to_timestamp(df, timestamp_col, minutes_col):
        return df.withColumn('approximate_arrival_time', 
            from_unixtime(
                unix_timestamp(col(timestamp_col)) + (col(minutes_col) * 60)
            )
        )

    # Example usage
    # Assuming df has 'current_time' and 'time_taken_for_distance' columns
    result_df = add_minutes_to_timestamp(df_with_times, 'current_time', 'time_taken_for_distance')
    result_df = result_df.withColumn('distance_km', ceil(col('distance_km')).cast('int'))

    result_df = result_df.select("bus_id", "route_id", "stop_id", "stop_name", "scheduled_time", "actual_arrival_time", "approximate_arrival_time", "distance_km")

    # Write output to Parquet
    result_df.write.mode("overwrite").parquet(output_file_path)
    spark.stop()
