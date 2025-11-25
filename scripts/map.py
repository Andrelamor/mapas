import geopandas as gpd
import matplotlib.pyplot as plt
from unidecode import unidecode
import os

# Verificar se o arquivo existe
geojson_path = "geojs-31-mun.json"
if not os.path.exists(geojson_path):
    raise FileNotFoundError(f"O arquivo {geojson_path} não foi encontrado. Verifique o caminho e tente novamente.")

# Carregar o GeoJSON
gdf = gpd.read_file(geojson_path)

# Normalizar os nomes removendo acentos
gdf["name"] = gdf["name"].apply(lambda x: unidecode(x.upper()))

# Lista de municípios a destacar
municipios_destacados = {
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
}

# Criar coluna de cores
gdf["color"] = gdf["name"].apply(lambda x: "red" if x in municipios_destacados else "lightgrey")

# Plotar o mapa
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color=gdf["color"], edgecolor="black", linewidth=0.3)
ax.set_title("Municípios Destacados em Vermelho", fontsize=14)
ax.axis("off")

# Salvar imagem do mapa
plt.savefig("mapa_municipios.png", dpi=300, bbox_inches="tight")
plt.show()