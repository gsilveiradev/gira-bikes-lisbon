# pip install psycopg2-binary requests

import psycopg2
import requests

# Database connection details
db_params = {
    "host": "localhost",
    "database": "gira_bikes",
    "user": "user",
    "password": "password"
}

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    print("Database connected successfully.")

    # Fetch data from the API
    response = requests.get("https://api.carrismetropolitana.pt/stops")
    response.raise_for_status()  # Check for request errors
    stops_data = response.json()

    # Insert data into the 'stops' table
    insert_query = """
        INSERT INTO carris_stops (
            id, district_id, district_name, lat, lon, locality, municipality_id, 
            municipality_name, operational_status, region_id, region_name, stop_id, location
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
    """

    for stop in stops_data:
        cursor.execute(insert_query, (
            stop["stop_id"], stop["district_id"], stop["district_name"], stop["lat"], stop["lon"], stop["locality"],
            stop["municipality_id"], stop["municipality_name"], stop["operational_status"], 
            stop["region_id"], stop["region_name"], stop["stop_id"],
            stop['lon'], stop['lat']  # For ST_MakePoint, we pass lon, lat again to create the geography
        ))

    # Commit the transaction
    connection.commit()
    print("Data inserted successfully.")

except (Exception, psycopg2.DatabaseError, requests.RequestException) as error:
    print("Error:", error)

finally:
    # Close the database connection
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")