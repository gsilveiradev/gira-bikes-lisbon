import psycopg2
import pandas as pd

# Database connection details
db_params = {
    "host": "localhost",
    "database": "gira_bikes",
    "user": "user",
    "password": "password"
}

# Output file paths
output_files = {
    "carris_stops": "carris_stops.csv",
    "distances_gira_metro": "distances_gira_metro.csv",
    "distances_gira_stops": "distances_gira_stops.csv",
    "distances_gira_train": "distances_gira_train.csv",
    "distances_gira_ciclovias_pontos": "distances_gira_ciclovias_pontos.csv",
    "gira_stations": "gira_stations.csv",
    "metro_stations": "metro_stations.csv",
    "train_stations": "train_stations.csv",
    "ciclovias": "ciclovias.csv",
    "ciclovias_pontos": "ciclovias_pontos.csv"
}

# Connect to the PostgreSQL database and export each table to a CSV file
try:
    connection = psycopg2.connect(**db_params)
    print("Database connected successfully.")

    for table_name, file_path in output_files.items():
        # Load data from the table into a pandas DataFrame
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, connection)
        
        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
        print(f"Data from {table_name} exported to {file_path}")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally:
    # Close the database connection
    if connection:
        connection.close()
        print("Database connection closed.")