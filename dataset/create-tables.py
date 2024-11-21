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
        CREATE TABLE carris_stops (
            id VARCHAR(50) PRIMARY KEY,
            district_id VARCHAR(50),
            district_name VARCHAR(100),
            locality VARCHAR(100),
            municipality_id VARCHAR(50),
            municipality_name VARCHAR(100),
            operational_status VARCHAR(50),
            region_id VARCHAR(50),
            region_name VARCHAR(100),
            stop_id VARCHAR(50),
            lat DOUBLE PRECISION NOT NULL,
            lon DOUBLE PRECISION NOT NULL,
            location geography(Point, 4326) NOT NULL
        );
        CREATE INDEX idx_cs_geo_position ON carris_stops USING GIST(geography(location));
        """,
        """
        CREATE TABLE train_stations (
            object_id VARCHAR(50) PRIMARY KEY,
            cod_sig VARCHAR(50),
            id_tipo VARCHAR(50),
            id VARCHAR(50),
            nome VARCHAR(100),
            global_id VARCHAR(100),
            lon DOUBLE PRECISION NOT NULL,
            lat DOUBLE PRECISION NOT NULL,
            location geography(Point, 4326) NOT NULL
        );
        CREATE INDEX idx_ts_geo_position ON train_stations USING GIST(geography(location));
        """,
        """
        CREATE TABLE metro_stations (
            object_id VARCHAR(50) PRIMARY KEY,
            cod_sig VARCHAR(50),
            id_tipo VARCHAR(50),
            nome VARCHAR(100),
            situacao VARCHAR(50),
            linha VARCHAR(50),
            global_id VARCHAR(100),
            lon DOUBLE PRECISION NOT NULL,
            lat DOUBLE PRECISION NOT NULL,
            location geography(Point, 4326) NOT NULL
        );
        CREATE INDEX idx_ms_geo_position ON metro_stations USING GIST(geography(location));
        """,
        """
        CREATE TABLE gira_stations (
            object_id VARCHAR(50) PRIMARY KEY,
            id_p VARCHAR(50),
            id_c VARCHAR(50),
            cod_via VARCHAR(50),
            nome_rua VARCHAR(100),
            ponto_referencia VARCHAR(100),
            freguesia VARCHAR(100),
            situacao VARCHAR(50),
            implantacao VARCHAR(50),
            global_id VARCHAR(100),
            lon DOUBLE PRECISION NOT NULL,
            lat DOUBLE PRECISION NOT NULL,
            location geography(Point, 4326) NOT NULL
        );
        CREATE INDEX idx_gs_geo_position ON gira_stations USING GIST(geography(location));
        """,
        """
        CREATE TABLE ciclovias (
            ciclovia_id VARCHAR(50) PRIMARY KEY,
            objectid VARCHAR(50),
            cod_sig VARCHAR(50),
            cod_via VARCHAR(50),
            cod_ciclovia VARCHAR(50),
            designacao VARCHAR(255),
            nome_projeto VARCHAR(255),
            hierarquia VARCHAR(50),
            eixo VARCHAR(255),
            tipologia VARCHAR(100),
            nivel_segregacao VARCHAR(100),
            tipo_intervencao VARCHAR(100),
            situacao VARCHAR(50),
            ano VARCHAR(50),
            entidade_resp VARCHAR(255),
            freguesia VARCHAR(100),
            comprimento DOUBLE PRECISION,
            comp_km DOUBLE PRECISION,
            idtipo VARCHAR(50),
            zonamento VARCHAR(255),
            globalid VARCHAR(100)
        );
        CREATE TABLE ciclovias_pontos (
            ciclovia_id VARCHAR(50),
            lat DOUBLE PRECISION NOT NULL,
            lon DOUBLE PRECISION NOT NULL,
            location geography(Point, 4326) NOT NULL
        );
        CREATE INDEX idx_ci_geo_position ON ciclovias_pontos USING GIST(geography(location));
        """,
    ]

    # Execute table creation queries
    for query in create_table_queries:
        cursor.execute(query)
    connection.commit()
    print("Tables created successfully.")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally:
    # Close the database connection
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")