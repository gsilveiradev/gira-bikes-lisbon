import psycopg2
import pandas as pd

# Database connection details
db_params = {
    "host": "localhost",
    "database": "gira_bikes",
    "user": "user",
    "password": "password"
}

# File paths for the CSV files
ciclovias_file = 'ciclovias.csv'
ciclovias_pontos_file = 'ciclovias_pontos.csv'

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    print("Database connected successfully.")

    # Load data from CSV files
    ciclovias_data = pd.read_csv(ciclovias_file)
    ciclovias_pontos_data = pd.read_csv(ciclovias_pontos_file)

    # Insert data into ciclovias table
    ciclovias_insert_query = """
        INSERT INTO ciclovias (
            objectid, cod_sig, cod_via, cod_ciclovia, designacao, nome_projeto, hierarquia, eixo, 
            tipologia, nivel_segregacao, tipo_intervencao, situacao, ano, entidade_resp, freguesia, 
            comprimento, comp_km, idtipo, zonamento, globalid, ciclovia_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for _, row in ciclovias_data.iterrows():
        cursor.execute(ciclovias_insert_query, (
            str(row['OBJECTID']), str(row['COD_SIG']), str(row['COD_VIA']), str(row['COD_CICLOVIA']), row['DESIGNACAO'], 
            row['NOME_PROJETO'], row['HIERARQUIA'], row['EIXO'], row['TIPOLOGIA'], 
            row['NIVEL_SEGREGACAO'], row['TIPO_INTERVENCAO'], row['SITUACAO'], str(row['ANO']), 
            row['ENTIDADE_RESP'], row['FREGUESIA'], row['COMPRIMENTO'], row['COMP_KM'], 
            row['IDTIPO'], row['ZONAMENTO'], row['GlobalID'], str(row['ciclovia_id'])
        ))

    # Insert data into ciclovias_pontos table
    ciclovias_pontos_insert_query = """
        INSERT INTO ciclovias_pontos (
            ciclovia_id, lat, lon, location
        ) VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
    """
    for _, row in ciclovias_pontos_data.iterrows():
        cursor.execute(ciclovias_pontos_insert_query, (
            int(row['ciclovia_id']), float(row['latitude']), float(row['longitude']), 
            float(row['longitude']), float(row['latitude'])  # Longitude comes first in ST_MakePoint
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
