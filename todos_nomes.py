import geopandas as gpd
import matplotlib.pyplot as plt
from unidecode import unidecode
import os

# Verificar se o arquivo existe
geojson_path = "brasil_completo.json"
if not os.path.exists(geojson_path):
    raise FileNotFoundError(f"O arquivo {geojson_path} não foi encontrado. Verifique o caminho e tente novamente.")

# Carregar o GeoJSON
gdf = gpd.read_file(geojson_path)

# Normalizar os nomes removendo acentos
gdf["name"] = gdf["name"].apply(lambda x: unidecode(x.upper()))

# Lista de estados a destacar
good = {"Recife","Salvador","Rio de Janeiro","Minas Gerais"}
bad = {"Vitória", "João Pessoa", "Amapá"}

# Função única de mapeamento de cores
def get_color(x):
    if x in bad:
        return "red"
    elif x in good:
        return "green"
    else:
        return "lightgrey"

# Aplicar cores
gdf["color"] = gdf["name"].apply(get_color)

# Plotar o mapa
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color=gdf["color"], edgecolor="black", linewidth=0.3)
#ax.set_title("Municípios Destacados em Vermelho", fontsize=14)
ax.axis("off")

# Salvar imagem do mapa
plt.savefig("brasil_todos.png", dpi=300, bbox_inches="tight")
plt.show()