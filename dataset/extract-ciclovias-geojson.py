import geopandas as gpd
import pandas as pd
import json

# Carregar o arquivo GeoJSON
geojson_path = "ciclovias.geojson"

# Ler o arquivo GeoJSON manualmente
with open(geojson_path, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Verificar e tratar geometrias nulas ou inválidas
ciclovias = []
ciclovias_pontos = []

for feature in geojson_data['features']:
    # Atributos gerais
    attributes = feature.get('properties', {})
    ciclovia_id = len(ciclovias)  # Gerar um ID único para cada ciclovia
    attributes['ciclovia_id'] = ciclovia_id
    ciclovias.append(attributes)

    # Coordenadas
    geometry = feature.get('geometry', None)
    if geometry is None or 'type' not in geometry or 'coordinates' not in geometry:
        continue  # Ignorar geometrias nulas ou inválidas

    if geometry['type'] == "LineString":
        for coord in geometry['coordinates']:
            ciclovias_pontos.append({
                "ciclovia_id": ciclovia_id,
                "latitude": coord[1],
                "longitude": coord[0]
            })
    elif geometry['type'] == "MultiLineString":
        for line in geometry['coordinates']:
            for coord in line:
                ciclovias_pontos.append({
                    "ciclovia_id": ciclovia_id,
                    "latitude": coord[1],
                    "longitude": coord[0]
                })

# Converter para DataFrame e salvar
ciclovias_df = pd.DataFrame(ciclovias)
ciclovias_pontos_df = pd.DataFrame(ciclovias_pontos)

# Salvar os arquivos CSV
ciclovias_csv_path = "ciclovias.csv"
ciclovias_pontos_csv_path = "ciclovias_pontos.csv"

ciclovias_df.to_csv(ciclovias_csv_path, index=False)
ciclovias_pontos_df.to_csv(ciclovias_pontos_csv_path, index=False)

ciclovias_csv_path, ciclovias_pontos_csv_path
