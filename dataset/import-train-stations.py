import psycopg2
import pandas as pd

# Database connection details
db_params = {
    "host": "localhost",
    "database": "gira_bikes",
    "user": "user",
    "password": "password"
}

# Load data from CSV file
csv_file_path = 'estacoes-comboios.csv'
data = pd.read_csv(csv_file_path)

# Connect to the PostgreSQL database and insert data
try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    print("Database connected successfully.")

    # SQL query to insert data into the estacoes_comboios table
    insert_query = """
        INSERT INTO train_stations (
            object_id, cod_sig, id_tipo, id, nome, global_id, lon, lat, location
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
    """

    # Insert each row into the database
    for _, row in data.iterrows():
        cursor.execute(insert_query, (
            str(row['ID']), str(row['COD_SIG']), str(row['IDTIPO']), str(row['ID']), row['NOME'],
            row['GlobalID'], row['lon'], row['lat'],
            row['lon'], row['lat']  # For ST_MakePoint, we pass lon, lat again to create the geography
        ))

    # Commit the transaction
    connection.commit()
    print("Data inserted successfully.")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally:
    # Close the database connection
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")