# mapa_brasil_notas.py
# Requisitos: geopandas, pandas, matplotlib, shapely
# pip install geopandas pandas matplotlib shapely

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import matplotlib as mpl

# --------- CONFIG ----------
# caminho para o GeoJSON/TopoJSON com os limites dos estados do Brasil
# substitua pelo caminho do seu arquivo 'brasil_completo.json' se tiver
PATH_BRAZIL_GEOJSON = "geojson-bases/brasil_amostra_sem_id.json"

# onde salvar a imagem resultante
OUTPUT_PNG = "mapa_brasil_notas.png"

# notas (0-20) conforme sua tabela
estado_notas = {
    "Minas Gerais": 12,
    "Goiás": 11,
    "Bahia": 10,
    "Rio Grande do Sul": 10,
    "Rio de Janeiro": 8,
    "Ceará": 7,
    "Pernambuco": 7,
    "Paraná": 7,
    "São Paulo": 7,
    "Amapá": 1
}

# municípios (nome, lon, lat, nota)
# coordenadas: (longitude, latitude)
municipios = [
    ("São Paulo", -46.6333, -23.5505, 9),
    ("Rio de Janeiro", -43.1729, -22.9068, 14),
    ("Belo Horizonte", -43.9345, -19.9167, 11),
    ("Vitória", -40.3128, -20.3155, 0),
    ("Fortaleza", -38.54306, -3.71722, 11),
    ("Salvador", -38.5016, -12.9777, 15),
    ("Recife", -34.8761, -8.04756, 15),
    ("João Pessoa", -34.8631, -7.11532, 3),
    ("Curitiba", -49.2733, -25.4284, 10),
    ("Porto Alegre", -51.2177, -30.0346, 9),
]

# --------- LEITURA DOS DADOS GEOGRÁFICOS ----------
# Leia o GeoJSON dos limites do Brasil. Espera-se um GeoDataFrame com uma coluna
# que identifica o nome do estado (ex: 'name' ou 'NM_ESTADO' etc).
gdf = gpd.read_file(PATH_BRAZIL_GEOJSON)
# Criar coluna de sigla a partir do 'id'
gdf["sigla"] = gdf["id"].str.upper().str.strip()

# Tente identificar automaticamente a coluna que contém o nome do estado:
possible_name_cols = ["name", "NAME", "NM_ESTADO", "nome", "uf", "sigla", "ESTADO", "NM_UF"]
name_col = None
for c in possible_name_cols:
    if c in gdf.columns:
        name_col = c
        break
if name_col is None:
    # se não encontrar, assume que a primeira coluna de texto é o nome
    for c in gdf.columns:
        if gdf[c].dtype == object:
            name_col = c
            break

if name_col is None:
    raise ValueError("Não consegui identificar coluna de nome do estado no seu GeoJSON. "
                     "Verifique o arquivo e informe qual coluna contém o nome do estado.")

# Padroniza nomes (remoção espaços extras)
gdf[name_col] = gdf[name_col].str.strip()

# --------- CRIAR coluna de nota para estados (default NaN) ----------
gdf["nota"] = gdf[name_col].map(estado_notas)

# --------- PREPARAR GeoDataFrame de municípios (pontos) ----------
mun_df = pd.DataFrame(municipios, columns=["nome", "lon", "lat", "nota"])
mun_df["geometry"] = [Point(xy) for xy in zip(mun_df.lon, mun_df.lat)]
mun_gdf = gpd.GeoDataFrame(mun_df, geometry="geometry", crs="EPSG:4326")

# Se o GeoDataFrame dos estados estiver em outra CRS, projete ambos para a mesma CRS
if gdf.crs is None:
    # assume EPSG:4326
    gdf = gdf.set_crs(epsg=4326)
if gdf.crs != mun_gdf.crs:
    mun_gdf = mun_gdf.to_crs(gdf.crs)

# --------- PLOTTING ----------
fig, ax = plt.subplots(1, 1, figsize=(10, 12))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# 1) Plota contorno dos estados (fronteira)
gdf.boundary.plot(ax=ax, linewidth=0.6, edgecolor="black", zorder=1)

# 2) Choropleth dos estados usando tons de verde
# definimos um colormap que seja uma variação de verde
cmap_estado = mpl.cm.get_cmap("Greens")  # variação do branco/verde escuro

# Para colorbar com escala 0-20 (mesma escala global)
vmin, vmax = 0, 20

# plot each state: geopandas pode mapear diretamente com a coluna 'nota'
# estados sem nota ficam em cor muito clara (quase branca)
gdf.plot(column="nota",
         cmap=cmap_estado,
         linewidth=0.2,
         ax=ax,
         edgecolor="black",
         zorder=2,
         vmin=vmin, vmax=vmax,
         missing_kwds={"color": "white", "edgecolor": "lightgrey", "hatch": None, "label": "Sem nota"})

# Plotar siglas no centro de cada estado
for idx, row in gdf.iterrows():
    x, y = row.geometry.centroid.x, row.geometry.centroid.y
    ax.text(x, y, row["sigla"], fontsize=9, fontweight="bold",
            ha="center", va="center", zorder=7, color="black")

# 3) Plot dos municípios: círculos azuis de mesmo tamanho, cor escala azul
# usamos colormap 'Blues' mapeado pela nota (0-20)
cmap_mun = mpl.cm.get_cmap("Blues")
norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
# tamanho fixo (em pontos^2)
marker_size = 140

# extrai coordenadas de cada ponto no sistema do eixo (proj)
xs = mun_gdf.geometry.x
ys = mun_gdf.geometry.y
# plota pontos com cor mapeada pela nota
for idx, row in mun_gdf.iterrows():
    nota = row["nota"]
    color = cmap_mun(norm(nota))
    ax.scatter(row.geometry.x, row.geometry.y,
               s=marker_size,
               color=color,
               edgecolor="black",
               linewidth=0.5,
               zorder=5)

# 4) Colorbars / legendas (eixos separados para evitar sobreposição)

# cria dois eixos auxiliares à direita do mapa
# [left, bottom, width, height] em coordenadas relativas da figura
cax_states = fig.add_axes([0.84, 0.30, 0.02, 0.40])   # estados
cax_muns   = fig.add_axes([0.92, 0.30, 0.02, 0.40])   # municípios

# colorbar para estados (verde)
sm_states = mpl.cm.ScalarMappable(
    cmap=cmap_estado,
    norm=mpl.colors.Normalize(vmin=vmin, vmax=vmax)
)
sm_states._A = []
cbar_states = fig.colorbar(sm_states, cax=cax_states)
cbar_states.set_label("Nota (estados)\nEscala 0–20", fontsize=9)

# colorbar para municípios (azul)
sm_muns = mpl.cm.ScalarMappable(
    cmap=cmap_mun,
    norm=mpl.colors.Normalize(vmin=vmin, vmax=vmax)
)
sm_muns._A = []
cbar_muns = fig.colorbar(sm_muns, cax=cax_muns)
cbar_muns.set_label("Nota (municípios)\nEscala 0–20", fontsize=9)


# 5) Rótulos opcionais dos municípios (pequeno deslocamento para não sobrepor)
for idx, row in mun_gdf.iterrows():
    ax.text(row.geometry.x + 0.8, row.geometry.y - 0.2, row["nome"],
            fontsize=8, fontweight="bold", zorder=6)

# Limpeza final: sem eixos
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_title("Desempenho dos critérios com observação 'completo' por estados e municípios selecionados", fontsize=12)

# ajuste da composição e salvar
plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Mapa salvo em:", OUTPUT_PNG)
plt.show()
