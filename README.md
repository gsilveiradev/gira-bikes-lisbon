# Gira Bikes Lisbon

Um estudo sobre a relação da integração das estações de bicicletas Gira com a rede de transporte público de Lisboa, incluindo ciclovias, paragens de autocarro e estações de Metro e Comboios.

## Contexto

Trabalho realizado para a disciplina de Bases de Dados Distribuidas Avançadas no [Mestrado em Ciência de Dados](https://iscte-iul.pt/curso/codigo/0329/mestrado-ciencia-de-dados) do ISCTE - Istituto Universitário de Lisboa.


# Datasets

- [GIRA - Bicicletas de Lisboa](https://dados.gov.pt/pt/datasets/gira-bicicletas-de-lisboa/)
- [POI Transportes](https://geodados-cml.hub.arcgis.com/maps/4933d8f832474ad2bff558cae59c5207/about)
  - [Estações de Comboio](https://geodados-cml.hub.arcgis.com/datasets/CML::poitransportes?layer=0)
  - [Estações de Metro](https://geodados-cml.hub.arcgis.com/datasets/CML::poitransportes?layer=1)
- [POI Mobilidade](https://geodados-cml.hub.arcgis.com/maps/440b7424a6284e0b9bf11179b95bf8d1/about)
  - [Rede Ciclável](https://geodados-cml.hub.arcgis.com/datasets/CML::ciclovias-2/explore?layer=0)
- [Carris Metropolitana](https://github.com/carrismetropolitana/api)
  - [Paragens de Autocarro](https://api.carrismetropolitana.pt/stops)

# Ferramentas auxiliares

## Postgres DB

A base de dados Postgres vai auxiliar no cálculo da distância entre os pontos que se quer relacionar, por exemplo:

- Distância entre estações Gira e:
  - Ciclovias
  - Paragens de autocarro
  - Estações de metro
  - Estações de comboios

## Docker

Usaremos contentores Docker para facilitar/automatizar o trabalho, neste caso iremos ter ferramentas auxiliares como:
- Postgres DB
- Scripts de importação com Python

Para executar o docker:

```sh
cd postgres
docker compose up -d
```

# Fazer Setup Inicial com Importações

É necessário estar na pasta `dataset` para executar os passos abaixo.

## 1. Criar tabelas no Postgres

Para criar as tabelas na base de dados Postgres, foi criado um script python que deve ser executado como no exemplo:

```sh
python3 create-tables.py
```

## 2. Importar Paragens de autocarro

Para importar as paragens de autocarro para a base de dados Postgres, foi criado um script python que deve ser executado como no exemplo:

```sh
python3 import-carris-stops.py
```

## 3. Importar Estações de Comboios

Para importar as estações de comboios para a base de dados Postgres, foi criado um script python que deve ser executado como no exemplo:

```sh
python3 import-train-stations.py
```

## 4. Importar Estações de Metro

Para importar as estações de metro para a base de dados Postgres, foi criado um script python que deve ser executado como no exemplo:

```sh
python3 import-metro-stations.py
```

## 5. Importar Estações Gira

Para importar as estações gira para a base de dados Postgres, foi criado um script python que deve ser executado como no exemplo:

```sh
python3 import-gira-stations.py
```

## 6. Importar Ciclovias

Para importar as ciclovias para a base de dados Postgres, foi criado um script python que deve ser executado como no exemplo:

```sh
python3 import-ciclovias.py
```

## 6. Calcular distâncias entre os pontos de interesse

Para calcular as distâncias entre as estações gira e os pontos de transporte público e importar para a base de dados Postgres, foi criado um script python que deve ser executado como no exemplo:

```sh
python3 calculate-distances.py
```

# Exportar todos os dados Postgres para CSV

Uma vez que os dados foram importados e calculados, para exportar tudo para arquivos CSV é preciso executar o script python como no exemplo abaixo.

É necessário estar na pasta `dataset/exported` para executar o script.

```sh
python3 export-postgres-to-csv.py
```

# Hadoop

A stack Hadoop utilizada neste trabalho será baseada em contentores Docker, referenciados no projeto [docker-hadoop-hive-parquet](https://github.com/tech4242/docker-hadoop-hive-parquet) e no artigo "[Making big moves in Big Data with Hadoop, Hive, Parquet, Hue and Docker](https://towardsdatascience.com/making-big-moves-in-big-data-with-hadoop-hive-parquet-hue-and-docker-320a52ca175)".

![hadoop-stack](hadoop/hadoop-stack.png)

Vamos assumir que temos criado uma Base de dados chamada `gira`, criada previamente através do Hue.

Além disso, vamos assumir que os arquivos CSV estarão presentes no path: `/user/admin/gira_data/`.

## Criar tabelas com Hue, no stack Hadoop

```
CREATE TABLE gira.gira_stations (
    object_id STRING,
    id_p STRING,
    id_c INT,
    cod_via INT,
    nome_rua STRING,
    ponto_referencia STRING,
    freguesia STRING,
    situacao STRING,
    implantacao STRING,
    global_id STRING,
    lon DOUBLE,
    lat DOUBLE,
    location STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/gira_stations.csv' INTO TABLE gira.gira_stations;
```

```
CREATE TABLE gira.metro_stations (
    object_id INT,
    cod_sig INT,
    id_tipo INT,
    nome STRING,
    situacao STRING,
    linha STRING,
    global_id STRING,
    lon DOUBLE,
    lat DOUBLE,
    location STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/metro_stations.csv' INTO TABLE gira.metro_stations;
```

```
CREATE TABLE gira.train_stations (
    object_id INT,
    cod_sig INT,
    id_tipo INT,
    id INT,
    nome STRING,
    global_id STRING,
    lon DOUBLE,
    lat DOUBLE,
    location STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/train_stations.csv' INTO TABLE gira.train_stations;
```

```
CREATE TABLE gira.carris_stops (
    id INT,
    district_id INT,
    district_name STRING,
    locality STRING,
    municipality_id INT,
    municipality_name STRING,
    operational_status STRING,
    region_id STRING,
    region_name STRING,
    stop_id INT,
    lat DOUBLE,
    lon DOUBLE,
    location STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/carris_stops.csv' INTO TABLE gira.carris_stops;
```

```
CREATE TABLE gira.distances_gira_metro (
    gira_id STRING,
    gira_nome_rua STRING,
    gira_freguesia STRING,
    metro_id INT,
    metro_nome STRING,
    distance_meters DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/distances_gira_metro.csv' INTO TABLE gira.distances_gira_metro;
```

```
CREATE TABLE gira.distances_gira_stops (
    gira_id STRING,
    gira_nome_rua STRING,
    gira_freguesia STRING,
    stops_id INT,
    stop_municipality_name STRING,
    distance_meters DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/distances_gira_stops.csv' INTO TABLE gira.distances_gira_stops;
```

```
CREATE TABLE gira.distances_gira_train (
    gira_id STRING,
    gira_nome_rua STRING,
    gira_freguesia STRING,
    train_id INT,
    train_nome STRING,
    distance_meters DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/distances_gira_train.csv' INTO TABLE gira.distances_gira_train;
```

```
CREATE TABLE gira.ciclovias_pontos (
    ciclovia_id STRING,
    lat DOUBLE,
    lon DOUBLE,
    location STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/ciclovias_pontos.csv' INTO TABLE gira.ciclovias_pontos;
```

```
CREATE TABLE gira.ciclovias (
    ciclovia_id STRING,
    objectid STRING,
    cod_sig STRING,
    cod_via STRING,
    cod_ciclovia STRING,
    designacao STRING,
    nome_projeto STRING,
    hierarquia STRING,
    eixo STRING,
    tipologia STRING,
    nivel_segregacao STRING,
    tipo_intervencao STRING,
    situacao STRING,
    ano STRING,
    entidade_resp STRING,
    freguesia STRING,
    comprimento DOUBLE,
    comp_km DOUBLE,
    idtipo STRING,
    zonamento STRING,
    globalid STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/ciclovias.csv' INTO TABLE gira.ciclovias;
```

```
CREATE TABLE gira.distances_gira_ciclovias_pontos (
    gira_id STRING,
    ciclovia_id STRING,
    distance_meters DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/user/admin/gira_data/distances_gira_ciclovias_pontos_split_01.csv' INTO TABLE gira.distances_gira_ciclovias_pontos;
LOAD DATA INPATH '/user/admin/gira_data/distances_gira_ciclovias_pontos_split_02.csv' INTO TABLE gira.distances_gira_ciclovias_pontos;
```