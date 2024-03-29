from datetime import date

import ee

ee.Initialize()

gridmet_transform = [
    0.041666666666666664, 0, -124.78749996666667,
    0, -0.041666666666666664, 49.42083333333334
]
asset_id = "projects/openet/ptjpl/ancillary/alpha/"
asset_version = "0.0.4"
gs_coll_id = "projects/openet/growing_season/gridmet/annual/gs_300_n2"

# Import dataset
dataset = ee.ImageCollection("projects/openet/ptjpl/ancillary/alpha/annual_sum")
data_sum = dataset.select(["dynamic_gs_eto_corr", "dynamic_gs_etw"]).sum()
gs_length = dataset.select("dynamic_gs_length").mean()

# Add mask based on GS length
mask = gs_length.unmask(1).lte(20)

dynamic_gs = (
    data_sum.select("dynamic_gs_eto_corr")
    .divide(data_sum.select("dynamic_gs_etw"))
    .rename("dynamic_gs")
)

dynamic_gs = dynamic_gs.updateMask(mask.Not())
dynamic_gs = dynamic_gs.unmask(1).rename("pt_eto_ratio").clamp(0.793650793, 2)

dynamic_gs = dynamic_gs\
    .set({"asset_version": asset_version,
          "bias_version": "0.2.0",
          "gs_collection": gs_coll_id,
          "date_ingested": date.today().strftime("%Y-%m-%d")})

task = ee.batch.Export.image.toAsset(
    image=ee.Image(dynamic_gs),
    description="Export GS ETo ETw",
    assetId=f"{asset_id}gridmet_1980-2020_dgs",
    dimensions='1386x585',
    crs='EPSG:4326',
    crsTransform=gridmet_transform,
    maxPixels=1e13
    )

try:
    task.start()
except:
    print("Error starting export task")
    print(task)
