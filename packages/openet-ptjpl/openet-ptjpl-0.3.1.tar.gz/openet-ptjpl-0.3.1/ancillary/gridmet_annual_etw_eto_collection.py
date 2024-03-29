from datetime import date

import numpy as np
import ee
import openet.refetgee

ee.Initialize()

''' ADD VERSION NUMBER !!!!!'''
# Calculate Annual ETw, ETo, and ET_corr sums based on growing season



# Ancillary variables
gridmet_transform = [0.041666666666666664, 0, -124.78749996666667, 0,
                     -0.041666666666666664, 49.42083333333334]
property_list = ["system:time_start"]
asset_id = "projects/openet/ptjpl/ancillary/alpha/annual_sum/"
yearList = np.arange(1981, 2021, 1)
assetVersion = "0.0.1"

# Functions


def gridmet_bias(img):
    eto = img.select("eto")
    month_str = img.date().format("MMM")
    bias = bias_ratio.filterMetadata("month_abbrev", "equals", month_str).first()
    return img.addBands(eto.multiply(bias).rename(["eto_corr"]))


def gridmet_etw(img):
    return img.addBands(
        ee.Image(openet.refetgee.Daily.gridmet(img, elev=elev_img, lat=lat_img).etw)
    )


def gridmet_doy(img):
    doy = ee.Number.parse(img.date().format("D"))
    return img.addBands(ee.Image(doy).rename("doy").int())


def mask_doy(img):
    start_mask = img.select("doy").gte(gsStart)
    end_mask = img.select("doy").lte(gsEnd)
    final_mask = start_mask.multiply(end_mask)
    return img.updateMask(final_mask).addBands(final_mask.rename(["mask"]))


# Import collections
gridmet_coll = ee.ImageCollection("IDAHO_EPSCOR/GRIDMET")

bias_ratio = ee.ImageCollection("projects/openet/reference_et/gridmet/ratios/v1/monthly/eto")

bias_version = bias_ratio.first().get("source_data_version").getInfo()

gs_coll_id = "projects/openet/growing_season/gridmet/annual/gs_300_n2"
gs_coll = ee.ImageCollection(gs_coll_id)  # has property year

# Project latitude array to match GRIDMET elevation grid exactly
elev_img = ee.Image("projects/climate-engine/gridmet/elevation")
lat_img = ee.Image.pixelLonLat().select('latitude')\
    .reproject('EPSG:4326', elev_img.projection().getInfo()['transform'])

# Set the output crs and crsTransform to match the GRIDMET images
gridmet_img = ee.Image('IDAHO_EPSCOR/GRIDMET/20180401')
crs = gridmet_img.projection().getInfo()['wkt']
geo = gridmet_img.projection().getInfo()['transform']

# Map etw, bias, and doy to griemt collection
etwColl = ee.ImageCollection(
    gridmet_coll.map(gridmet_etw).map(gridmet_bias).map(gridmet_doy)
    .select(["eto", "eto_corr", "etw", "doy"])
)

# Filter by year
exportImgList = []

for year in yearList:
    # Filter Gridmet collection
    startDate = ee.Date.fromYMD(int(year), 1, 1)
    endDate = ee.Date.fromYMD(int(year)+1, 1, 1)
    gridmetYear = etwColl.filterDate(startDate, endDate)

    # Filter Drowing season image
    gsYear = gs.filterMetadata("year", "equals", int(year)).first()
    gsStart = gsYear.select("start_doy")
    gsEnd = gsYear.select("end_doy")

    # Growing season Sum
    gsSum = gridmetYear.map(mask_doy).sum()\
        .select(["eto", "eto_corr", "etw", "mask"],
                ["dynamic_gs_eto", "dynamic_gs_eto_corr",
                 "dynamic_gs_etw", "dynamic_gs_length"])

    # Annual Sum
    annualSum = gridmetYear.sum()\
        .select(["eto", "eto_corr", "etw"],
                ["annual_eto", "annual_eto_corr", "annual_etw"])

    # Apr-Sep Sum
    aprSepSum = (
        gridmetYear.filterDate(
            ee.Date.fromYMD(int(year), 4, 1), ee.Date.fromYMD(int(year), 10, 1))
        .sum()
        .select(["eto", "eto_corr", "etw"],
                ["apr_sep_eto", "apr_sep_eto_corr", "apr_sep_etw"])
    )

    # Apr-Oct Sum
    aprOctSum = (
        gridmetYear.filterDate(
            ee.Date.fromYMD(int(year), 4, 1), ee.Date.fromYMD(int(year), 11, 1))
        .sum()
        .select(["eto", "eto_corr", "etw"],
                ["apr_oct_eto", "apr_oct_eto_corr", "apr_oct_etw"])
    )

    export_img = gsSum.addBands(annualSum).addBands(aprSepSum)\
        .addBands(aprOctSum)\
        .copyProperties(gridmetYear.first(), property_list)\
        .set({"asset_version": assetVersion,
              "bias_version": biasVersion,
              "gs_collection": gs_coll_id,
              "date_ingested": date.today().strftime("%Y-%m-%d"),
              "year": int(year)})

    # export image to collection
    task = ee.batch.Export.image.toAsset(
        image=ee.Image(export_img),
        description=f"Export: {str(year)}",
        assetId=f"{asset_id}{str(year)}",
        dimensions='1386x585',
        crs='EPSG:4326',
        crsTransform=gridmet_transform,
        maxPixels=1e13,
        )

    try:
        task.start()
    except:
        print("Error starting export task")
        print(task)
