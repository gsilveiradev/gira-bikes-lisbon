import psycopg2
import pandas as pd

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

    # Create tables to store distances
    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS distances_gira_train (
            gira_id VARCHAR(50),
            gira_nome_rua VARCHAR(100),
            gira_freguesia VARCHAR(100),
            train_id VARCHAR(50),
            train_nome VARCHAR(100),
            distance_meters DOUBLE PRECISION
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS distances_gira_metro (
            gira_id VARCHAR(50),
            gira_nome_rua VARCHAR(100),
            gira_freguesia VARCHAR(100),
            metro_id VARCHAR(50),
            metro_nome VARCHAR(100),
            distance_meters DOUBLE PRECISION
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS distances_gira_stops (
            gira_id VARCHAR(50),
            gira_nome_rua VARCHAR(100),
            gira_freguesia VARCHAR(100),
            stops_id VARCHAR(50),
            stop_municipality_name VARCHAR(100),
            distance_meters DOUBLE PRECISION
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS distances_gira_ciclovias_pontos (
            gira_id VARCHAR(50),
            ciclovia_id VARCHAR(50),
            distance_meters DOUBLE PRECISION
        );
        """
    ]

    # Execute table creation queries
    for query in create_table_queries:
        cursor.execute(query)
    connection.commit()

    # Query and insert distances from estacoes_gira to estacoes_comboios
    distance_comboios_query = """
        INSERT INTO distances_gira_train (gira_id, gira_nome_rua, gira_freguesia, train_id, train_nome, distance_meters)
        SELECT g.id_p AS gira_id, g.nome_rua AS gira_nome_rua, g.freguesia AS gira_freguesia, c.id AS train_id, c.nome AS train_nome,
               ST_Distance(g.location, c.location) AS distance_meters
        FROM gira_stations AS g
        JOIN train_stations AS c
        ON ST_DWithin(g.location, c.location, 10000);
    """
    cursor.execute(distance_comboios_query)
    connection.commit()
    print("Distances to train_stations saved.")

    # Query and insert distances from estacoes_gira to estacoes_metro
    distance_metro_query = """
        INSERT INTO distances_gira_metro (gira_id, gira_nome_rua, gira_freguesia, metro_id, metro_nome, distance_meters)
        SELECT g.id_p AS gira_id, g.nome_rua AS gira_nome_rua, g.freguesia AS gira_freguesia, m.cod_sig AS metro_id, m.nome AS metro_nome,
               ST_Distance(g.location, m.location) AS distance_meters
        FROM gira_stations AS g
        JOIN metro_stations AS m
        ON ST_DWithin(g.location, m.location, 10000);
    """
    cursor.execute(distance_metro_query)
    connection.commit()
    print("Distances to metro_stations saved.")

    # Query and insert distances from estacoes_gira to estacoes_stops
    distance_stops_query = """
        INSERT INTO distances_gira_stops (gira_id, gira_nome_rua, gira_freguesia, stops_id, stop_municipality_name, distance_meters)
        SELECT g.id_p AS gira_id, g.nome_rua AS gira_nome_rua, g.freguesia AS gira_freguesia, s.stop_id AS stops_id, s.municipality_name as stop_municipality_name,
               ST_Distance(g.location, s.location) AS distance_meters
        FROM gira_stations AS g
        JOIN carris_stops AS s
        ON ST_DWithin(g.location, s.location, 10000);
    """
    cursor.execute(distance_stops_query)
    connection.commit()
    print("Distances to carris_tops saved.")

    # Query and insert distances from estacoes_gira to estacoes_stops
    distance_stops_query = """
        INSERT INTO distances_gira_ciclovias_pontos (gira_id, ciclovia_id, distance_meters)
        SELECT g.id_p AS gira_id, cp.ciclovia_id AS ciclovia_id, 
                ST_Distance(g.location, cp.location) AS distance_meters
            FROM gira_stations AS g
            JOIN ciclovias_pontos AS cp ON ST_DWithin(g.location, cp.location, 10000);
    """
    cursor.execute(distance_stops_query)
    connection.commit()
    print("Distances to carris_tops saved.")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally:
    # Close the database connection
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")