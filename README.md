✅ 1. Instalar as bibliotecas necessárias
Abra seu terminal (ou prompt de comando) e execute:

bash
Copiar
Editar
pip install geopandas matplotlib shapely
✅ 2. Salve o arquivo GeoJSON
Salve o arquivo geojs-31-mun.json (você já tem!) em uma pasta acessível. Guarde o caminho do arquivo — por exemplo: C:/meus_arquivos/geojs-31-mun.json.

✅ 3. Código Python para gerar o mapa
python
Copiar
Editar
import geopandas as gpd
import matplotlib.pyplot as plt
import json
from shapely.geometry import shape
from geopandas import GeoDataFrame, GeoSeries

# Caminho para seu arquivo GeoJSON
geojson_path = "C:/meus_arquivos/geojs-31-mun.json"

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
    "BELO HORIZONTE", "TRÊS CORAÇÕES", "BETIM", "BAMBUÍ", "UBÁ", "BARBACENA", "SABARÁ",
    "PATOS DE MINAS", "JUIZ DE FORA", "ÁGUAS FORMOSAS", "ALÉM PARAÍBA", "ANDRADAS",
    "ARAXÁ", "BOM DESPACHO", "BRASÍLIA DE MINAS", "BRUMADINHO", "CAMPO BELO",
    "CARATINGA", "CONTAGEM", "CORAÇÃO DE JESUS", "CURVELO", "DIAMANTINA", "FORMIGA",
    "FRANCISCO SÁ", "FRUTAL", "GUANHÃES", "IBIRITÉ", "IPATINGA", "ITABIRA", "ITAJUBÁ",
    "ITAMBACURI", "ITUIUTABA", "JACUTINGA", "JANAÚBA", "JANUÁRIA", "LAGOA DA PRATA",
    "MALACACHETA", "MANGA", "MANHUMIRIM", "MANTENA", "MARTINHO CAMPOS", "MINAS NOVAS",
    "MONTES CLAROS", "MURIAÉ", "NANUQUE", "PADRE PARAÍSO", "PARÁ DE MINAS", "PARACATU",
    "PATROCÍNIO", "PEDRA AZUL", "PERDÕES", "PIRAPORA", "PIUMHI", "PONTE NOVA",
    "POUSO ALEGRE", "RIBEIRÃO DAS NEVES", "SALINAS", "SANTO ANTÔNIO DO AMPARO",
    "SANTO ANTÔNIO DO MONTE", "SANTOS DUMONT", "SÃO DOMINGOS DO PRATA",
    "SÃO JOÃO NEPOMUCENO", "SÃO LOURENÇO", "SÃO SEBASTIÃO DO PARAÍSO", "SETE LAGOAS",
    "TEÓFILO OTONI", "TIMÓTEO", "TRÊS PONTAS", "UBERABA", "UBERLÂNDIA", "VARGINHA",
    "VIÇOSA", "ALFENAS", "CORONEL FABRICIANO", "DIVINÓPOLIS", "GOVERNADOR VALADARES",
    "LEOPOLDINA", "SÃO JOÃO DEL REI", "UNAÍ"
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
Se quiser, posso te ajudar a salvar o mapa como imagem, ou até criar uma versão interativa com folium.

Quer fazer isso também?







Você disse:
Sim


O ChatGPT disse:
Ótimo! Vamos fazer duas coisas agora:

Gerar um mapa interativo com folium, que você pode visualizar no navegador e compartilhar.

Salvar como imagem (PNG) usando matplotlib.

✅ 1. Instalar o folium
No terminal:

bash
Copiar
Editar
pip install folium
✅ 2. Código para gerar mapa interativo e salvar como HTML
python
Copiar
Editar
import folium
from shapely.geometry import mapping

# Centro aproximado de MG
centro_mg = [-18.5, -44.5]

# Criar o mapa
mapa = folium.Map(location=centro_mg, zoom_start=6)

# Adicionar municípios
for _, row in gdf.iterrows():
    cor = "red" if row["NM_MUNICIP"] in municipios_destacados else "#d3d3d3"
    folium.GeoJson(
        mapping(row["geometry"]),
        style_function=lambda x, cor=cor: {
            'fillColor': cor,
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7
        },
        tooltip=row["NM_MUNICIP"]
    ).add_to(mapa)

# Salvar como HTML
mapa.save("mapa_mg_interativo.html")
print("Mapa interativo salvo como 'mapa_mg_interativo.html'")
Depois, basta abrir o arquivo mapa_mg_interativo.html no navegador.

✅ 3. Salvar o mapa como imagem (PNG)
Você já viu a visualização com matplotlib. Para salvar em vez de mostrar:

python
Copiar
Editar
# Salvar como imagem PNG
fig, ax = plt.subplots(figsize=(12, 12))
gdf.plot(ax=ax, color=gdf["cor"], edgecolor="black", linewidth=0.2)
ax.set_title("Municípios de MG destacados em vermelho", fontsize=14)
ax.axis("off")

plt.tight_layout()
plt.savefig("mapa_mg_destacado.png", dpi=300)
print("Imagem salva como 'mapa_mg_destacado.png'")
