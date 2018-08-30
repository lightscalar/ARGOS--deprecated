from geo_utils import *

from osgeo import gdal, osr
from skimage.io import imread
from pylab import imsave


if __name__ == "__main__":

    filename = "DJI_0468.JPG"
    img = imread(filename)[0]
    h, w, l = img.shape
    control_pts = [
        (h / 2, w / 2),
        (h / 2, w / 2 + 500),
        (h / 2 + 500, w / 2),
        (h / 2 + 500, w / 2 + 500),
    ]
    # control_pts = [(0,0), (h,0), (h,w), (0,w)]

    # gcp_list = [
    #     (np.random.randint(img.shape[0]), np.random.randint(img.shape[1]))
    #     for _ in range(4)
    # ]

    gcps = []
    for gcp in control_pts:
        lat, lon = pixel_to_lat_lon(gcp[0], gcp[1], filename)
        gcps.append(gdal.GCP(lon, lat, 0, gcp[1], gcp[0]))

    # Save as a PDF.
    output_file = "geo_referenced.pdf"
    imsave(output_file, img)

    # Attach all the georeference information.
    ds = gdal.Open(output_file, gdal.GA_Update)
    sr = osr.SpatialReference()
    sr.SetWellKnownGeogCS("WGS84")

    # ds.SetGCPs(sr.ExportToWkt())
    ds.SetGCPs(gcps, sr.ExportToWkt())
    # ds.SetProjection(sr.ExportToWkt())
    # ds.SetGeoTransform(gdal.GCPsToGeoTransform(gcps))
    ds = None
