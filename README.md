# Gira Bikes Lisbon

Um estudo sobre a integração das estações de bicicletas Gira com a rede de transporte público de Lisboa, incluindo ciclovias, paragens de autocarro e estações de Metro e Comboios.

## Contexto

Trabalho realizado para a disciplina de Bases de Dados Distribuídas Avançadas no [Mestrado em Ciência de Dados](https://iscte-iul.pt/curso/codigo/0329/mestrado-ciencia-de-dados) do ISCTE - Instituto Universitário de Lisboa.

# 1) Preparação dos Datasets

Para este estudo ser desenvolvido, foi necessário utilizar datasets de diferentes fontes, tais como:

1) [Dados.gov](https://dados.gov.pt/pt/) - Plataforma aberta para dados públicos portugueses.
   - [GIRA - Bicicletas de Lisboa](https://dados.gov.pt/pt/datasets/gira-bicicletas-de-lisboa/): Dados sobre as estações Gira, incluindo localização, estado e capacidade.
2) [Geodados CML](https://geodados-cml.hub.arcgis.com/) - Plataforma de dados abertos georreferenciados da Câmara Municipal de Lisboa.
   - [POI Transportes](https://geodados-cml.hub.arcgis.com/maps/4933d8f832474ad2bff558cae59c5207/about) - Serviço de mapa com indicação das principais estações de transportes, interfaces fluviais, elevadores e ascensores, postos de carregamento Mobi E de Lisboa, Zonas de Emissões Reduzidas.
     - [Estações de Comboio](https://geodados-cml.hub.arcgis.com/datasets/CML::poitransportes?layer=0): Dados sobre as estações de comboio, incluindo localização e nome.
     - [Estações de Metro](https://geodados-cml.hub.arcgis.com/datasets/CML::poitransportes?layer=1): Dados sobre as estações de metro, incluindo localização e nome.
   - [POI Mobilidade](https://geodados-cml.hub.arcgis.com/maps/440b7424a6284e0b9bf11179b95bf8d1/about) - Serviço de mapa de área de zonamento de mobilidade em Lisboa.
     - [Rede Ciclável](https://geodados-cml.hub.arcgis.com/datasets/CML::ciclovias-2/explore?layer=0): Dados sobre as ciclovias, incluindo localização e nome.
3) [Carris Metropolitana API](https://github.com/carrismetropolitana/api) - Um serviço de código aberto que fornece informações de rede no formato JSON ou Protocol Buffers. Este serviço lê e converte o arquivo GTFS oficial da Carris Metropolitana.
   - [Paragens de Autocarro](https://github.com/carrismetropolitana/api?tab=readme-ov-file#stops): Retorna informações estáticas para todas as paragens de autocarros Carris, bem como linhas, rotas e padrões associados que usam cada paragem. 

![datasets](dataset/dataset-gira-fontes.png)

## 1.1) Ferramentas Auxiliares

Para facilitar a importação dos datasets e posterior preparação dos dados, foi necessário utilizar uma base de dados Postgres com [PostGIS](https://postgis.net/).

Essa base de dados foi criada num contentor Docker, para facilitar a sua execução e utilização, a qual pode ser encontrada na pasta `postgres`.

Para executar o contentor Docker, basta entrar na pasta `postgres` e executar o comando:

```sh
docker compose up -d
```

A base de dados Postgres vai possibilitar a importação de todos os datasets, de diferentes fontes, formatos e estruturas, para um único formato. 

Posteriormente, com o auxílio da extensão PostGIS, será executado o cálculo de distâncias entre os pontos de interesse, e a posterior exportação dos dados para arquivos CSV.

## 1.2) Importação dos Datasets

Os datasets foram baixados das fontes acima e armazenados na pasta `dataset`, sendo cada um deles:

- [ciclovias.geojson](dataset/ciclovias.geojson) - Dados sobre as ciclovias de Lisboa.
- [estacoes-comboios.csv](dataset/estacoes-comboios.csv) - Dados sobre as estações de comboio de Lisboa.
- [estacoes-gira.csv](dataset/estacoes-gira.csv) - Dados sobre as estações Gira de Lisboa.
- [estacoes-metro.csv](dataset/estacoes-metro.csv) - Dados sobre as estações de metro de Lisboa.

> Para executar os scripts abaixo, é necessário estar no diretório `dataset`.

Os dados das paragens de autocarro foram obtidos através da API REST da Carris Metropolitana e inseridos diretamente na base de dados Postgres, ao executar o script python:

```sh
python3 import-carris-stops.py
```

Todos os outros ficheiros CSV e GeoJSON foram importados para a base de dados Postgres, ao executar os respetivos scripts python:

**Extrair ciclovias do GeoJSON para CSV:**
```sh
python3 extract-ciclovias-geojson.py
```

**Importar ciclovias do CSV para Postgres:**
```sh
python3 import-ciclovias.py
```

**Importar estações Gira do CSV para Postgres:**
```sh
python3 import-gira-stations.py
```

**Importar estações de Metro do CSV para Postgres:**
```sh
python3 import-metro-stations.py
```

**Importar estações de Comboio do CSV para Postgres:**
```sh
python3 import-train-stations.py
```

Ao final deste processo, todos os dados dos datasets foram importados para a base de dados Postgres, e estão prontos para serem utilizados. A imagem abaixo resume o relacionamento entre os dados importados.

![Relação dos Datasets](dataset/dataset-gira-relationships.png)

## 1.3) Cálculo de Distâncias

Uma vez que os dados estão importados na base de dados Postgres, é necessário calcular a distância entre os pontos de interesse.

A imagem abaixo ilustra o cálculo que vai ser preciso fazer para obter a distância - em metros - entre as estações Gira e os pontos de transporte público.

![Distâncias](dataset/dataset-gira-distances.png)

> Para executar os scripts abaixo, é necessário estar no diretório `dataset`.

Para calcular as distâncias entre as estações Gira e os pontos de transporte público, foi criado um script python que deve ser executado como no exemplo:

```sh
python3 calculate-distances.py
```

O script acima vai criar tabelas de distâncias no Postgres e calcular a distância em metros entre as estações Gira e todos os outros pontos de transporte público.

## 1.4) Exportação dos Dados para ficheiros CSV

Uma vez que todos os dados estão importados e as distâncias calculadas, é necessário exportar todos os dados para arquivos CSV, para que possam ser importados para o Hadoop.

> Para executar os scripts abaixo, é necessário estar no diretório `exported`.

Para exportar todos os dados da base de dados Postgres para arquivos CSV, foi criado um script python que deve ser executado como no exemplo:

```sh
python3 export-postgres-to-csv.py
```

Ao final deste processo, todos os dados importados e calculados na base de dados Postgres foram exportados para arquivos CSV, e estão prontos para serem importados para o Hadoop.

A imagem abaixo ilustra o processo de importação e preparação dos datasets:

![importação dos datasets](dataset/dataset-gira-importacao.png)

# 2) Hadoop

A stack Hadoop utilizada neste trabalho será baseada em contentores Docker, referenciados no projeto [docker-hadoop-hive-parquet](https://github.com/tech4242/docker-hadoop-hive-parquet) e no artigo "[Making big moves in Big Data with Hadoop, Hive, Parquet, Hue and Docker](https://towardsdatascience.com/making-big-moves-in-big-data-with-hadoop-hive-parquet-hue-and-docker-320a52ca175)".

![hadoop-stack](hadoop/hadoop-ecosystem-gira.png)

## 2.1) Aceder ao Hue e criar user Admin

O primeiro passo é aceder ao Hue, que é uma interface gráfica para o Hadoop, e criar um user Admin - sugestão usada no escopo deste trabalho.

Abrir http://localhost:8888/ e criar um user `admin` com password `admin`.

## 2.2) Copiar datasets para o HDFS com comandos Docker

**Entrar no diretório `hadoop`**

```shell
cd hadoop
```

**Criar diretório `/datasets` no HDFS**

```shell
docker exec hadoop-namenode-1 /bin/bash hdfs dfs -mkdir /datasets
```

**Copiar datasets finais para o contentor docker**

```shell
docker cp ../dataset/exported/ hadoop-namenode-1:/
```

**Inserir os datasets no sistema de ficheiros do Hadoop (HDFS)**

```shell
docker exec hadoop-namenode-1 /bin/bash hdfs dfs -put /exported /datasets
```
A imagem abaixo ilustra o que acontece ao executar os comandos acima.

![hadoop-upload-csv-docker](hadoop/hadoop-upload-csv-docker.png)

### 2.2.1) Alternativa: Copiar datasets para o HDFS com Hue

Em alternativa, o upload dos datasets para o HDFS pode ser feito através da interface gráfica do Hue, que no caso deste trabalho está disponível em http://localhost:8888/.

A imagem abaixo ilustra o que acontece ao fazer o upload dos datasets para o HDFS através do Hue.

![hadoop-upload-csv-hue](hadoop/hadoop-upload-csv-hue.png)

## 2.3) Criar tabelas no Hive com Hue

Vamos assumir que temos criado uma Base de dados chamada `default`.

Além disso, vamos assumir que os arquivos CSV estarão presentes no path: `/datasets/exported/`.

```
CREATE TABLE gira_stations (
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

LOAD DATA INPATH '/datasets/exported/gira_stations.csv' INTO TABLE gira_stations;
```

```
CREATE TABLE metro_stations (
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

LOAD DATA INPATH '/datasets/exported/metro_stations.csv' INTO TABLE metro_stations;
```

```
CREATE TABLE train_stations (
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

LOAD DATA INPATH '/datasets/exported/train_stations.csv' INTO TABLE train_stations;
```

```
CREATE TABLE carris_stops (
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

LOAD DATA INPATH '/datasets/exported/carris_stops.csv' INTO TABLE carris_stops;
```

```
CREATE TABLE distances_gira_metro (
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

LOAD DATA INPATH '/datasets/exported/distances_gira_metro.csv' INTO TABLE distances_gira_metro;
```

```
CREATE TABLE distances_gira_stops (
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

LOAD DATA INPATH '/datasets/exported/distances_gira_stops.csv' INTO TABLE distances_gira_stops;
```

```
CREATE TABLE distances_gira_train (
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

LOAD DATA INPATH '/datasets/exported/distances_gira_train.csv' INTO TABLE distances_gira_train;
```

```
CREATE TABLE ciclovias_pontos (
    ciclovia_id STRING,
    lat DOUBLE,
    lon DOUBLE,
    location STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/datasets/exported/ciclovias_pontos.csv' INTO TABLE ciclovias_pontos;
```

```
CREATE TABLE ciclovias (
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

LOAD DATA INPATH '/datasets/exported/ciclovias.csv' INTO TABLE ciclovias;
```

```
CREATE TABLE distances_gira_ciclovias_pontos (
    gira_id STRING,
    ciclovia_id STRING,
    distance_meters DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '/datasets/exported/distances_gira_ciclovias_pontos.csv' INTO TABLE distances_gira_ciclovias_pontos;
```