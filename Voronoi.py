import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np

from scipy.spatial import Voronoi
from pathlib import Path


# carregar database
base_path = Path(__file__).parent
file_path = base_path / "opendatabcn_esports_instalacions-esportives.csv"

df = pd.read_csv(file_path, encoding='utf-16', sep=',')

# netejar noms
df.columns = df.columns.str.strip()

# eliminar buits
df = df.dropna(subset=['geo_epgs_4326_lon', 'geo_epgs_4326_lat'])

# identificar longituds i latituds
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(
        df['geo_epgs_4326_lon'],
        df['geo_epgs_4326_lat']
    ),
    crs="EPSG:4326"
)

# transformar a sistema mètric
gdf = gdf.to_crs(epsg=3857)

# reduir punts
gdf = gdf.sample(30, random_state=1)

# VORONOI
points = np.array([(geom.x, geom.y) for geom in gdf.geometry])
vor = Voronoi(points)

# límits
min_x, min_y, max_x, max_y = gdf.total_bounds

# PLOT
fig, ax = plt.subplots(figsize=(10, 10))

# punts
gdf.plot(ax=ax, color='red', markersize=10, alpha=0.7)

# Voronoi net 
for region in vor.regions:
    if not region or -1 in region:
        continue

    polygon = [vor.vertices[i] for i in region]

    # només dibuixar si està dins la zona
    if all(min_x <= x <= max_x and min_y <= y <= max_y for x, y in polygon):
        xs, ys = zip(*(polygon + [polygon[0]]))
        ax.plot(xs, ys, color='black', linewidth=1, alpha=0.7)

# mapa base
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

# ajustar vista
ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)

# netejar eixos
ax.axis('off')

# títol
plt.title("Àrees d'influència de les instal·lacions esportives (Voronoi)", fontsize=14)

# guardar
plt.savefig("voronoi_map.png", dpi=300, bbox_inches='tight')

plt.show()