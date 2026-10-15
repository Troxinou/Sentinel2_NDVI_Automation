import rasterio
import numpy as np

red_band_path = 'data/B04.tif'
nir_band_path = 'data/B08.tif'
output_ndvi_path = 'results/NDVI_Output.tif'

print("Lecture des images Sentinel-2 (TIF)...")

with rasterio.open(red_band_path) as red_src:
    red_data = red_src.read(1).astype('float32')
    profile = red_src.profile

with rasterio.open(nir_band_path) as nir_src:
    nir_data = nir_src.read(1).astype('float32')

print("Calcul de l'indice de végétation (NDVI)...")

np.seterr(divide='ignore', invalid='ignore')
ndvi = np.where(
    (nir_data + red_data) == 0.,
    0,
    (nir_data - red_data) / (nir_data + red_data)
)

print(f"Sauvegarde dans {output_ndvi_path}...")

profile.update(driver='GTiff', dtype=rasterio.float32, count=1)
with rasterio.open(output_ndvi_path, 'w', **profile) as dst:
    dst.write(ndvi, 1)

print("Opération terminée avec succès !")