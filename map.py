import geopandas as gpd
import matplotlib.pyplot as plt
import json
from shapely.geometry import shape
from geopandas import GeoDataFrame, GeoSeries

# Caminho para seu arquivo GeoJSON
geojson_path = "geojs-31-mun.json"

# Abrir e carregar os dados manualmente
with open(geojson_path, encoding='utf-8') as f:
    data = json.load(f)

# Extrair geometrias e propriedades
geometrias = [shape(feat["geometry"]) for feat in data["features"]]
propriedades = [feat["properties"] for feat in data["features"]]

# Criar GeoDataFrame
gdf = GeoDataFrame(propriedades, geometry=GeoSeries(geometrias), crs="EPSG:4674")

# Lista de municípios (em maiúsculas)
municipios_destacados = [
    "BELO HORIZONTE", "TRES CORACOES", "BETIM", "BAMBUI", "UBA", "BARBACENA", "SABARA",
    "PATOS DE MINAS", "JUIZ DE FORA", "AGUAS FORMOSAS", "ALEM PARAIBA", "ANDRADAS",
    "ARAXA", "BOM DESPACHO", "BRASILIA DE MINAS", "BRUMADINHO", "CAMPO BELO",
    "CARATINGA", "CONTAGEM", "CORACAO DE JESUS", "CURVELO", "DIAMANTINA", "FORMIGA",
    "FRANCISCO SA", "FRUTAL", "GUANHAES", "IBIRITE", "IPATINGA", "ITABIRA", "ITAJUBA",
    "ITAMBACURI", "ITUIUTABA", "JACUTINGA", "JANAUBA", "JANUARIA", "LAGOA DA PRATA",
    "MALACACHETA", "MANGA", "MANHUMIRIM", "MANTENA", "MARTINHO CAMPOS", "MINAS NOVAS",
    "MONTES CLAROS", "MURIAE", "NANUQUE", "PADRE PARAISO", "PARA DE MINAS", "PARACATU",
    "PATROCINIO", "PEDRA AZUL", "PERDOES", "PIRAPORA", "PIUMHI", "PONTE NOVA",
    "POUSO ALEGRE", "RIBEIRAO DAS NEVES", "SALINAS", "SANTO ANTONIO DO AMPARO",
    "SANTO ANTONIO DO MONTE", "SANTOS DUMONT", "SAO DOMINGOS DO PRATA",
    "SAO JOAO NEPOMUCENO", "SAO LOURENCO", "SAO SEBASTIAO DO PARAISO", "SETE LAGOAS",
    "TEOFILO OTONI", "TIMOTEO", "TRES PONTAS", "UBERABA", "UBERLANDIA", "VARGINHA",
    "VICOSA", "ALFENAS", "CORONEL FABRICIANO", "DIVINOPOLIS", "GOVERNADOR VALADARES",
    "LEOPOLDINA", "SAO JOAO DEL REI", "UNAI"
]


# Padronizar os nomes
gdf["NM_MUNICIP"] = gdf["NM_MUNICIP"].str.upper()

# Definir cor por município
gdf["cor"] = gdf["NM_MUNICIP"].apply(lambda nome: "red" if nome in municipios_destacados else "lightgrey")

# Plotar
fig, ax = plt.subplots(figsize=(12, 12))
gdf.plot(ax=ax, color=gdf["cor"], edgecolor="black", linewidth=0.3)
ax.set_title("Municípios de MG destacados em vermelho", fontsize=14)
ax.axis("off")

plt.tight_layout()
plt.show()
