'''

    Find the latitude, longitude position of any pixel in a georeferenced tif file.

'''

from osgeo import gdal, osr
import numpy as np


def transform_geodetic_to_latlon(ds, x, y):
    '''Transform geodetic coordinates to latitude, longitude, altitude tuples.'''

    source = osr.SpatialReference()
    source.ImportFromWkt(ds.GetProjection())

    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(source, target)
    return transform.TransformPoint(x, y)


def pixel_to_coord(ds, col, row):
    '''Convert column and row indices to geodetic coordinates.'''

    x_upper_left, xres, xskew, y_upper_left, yskew, yres = ds.GetGeoTransform()

    lon = (xres * col) + (xskew * row) + x_upper_left
    lat = (yskew * col) + (yres * row) + y_upper_left

    return lon, lat


def coord_to_pixel(ds, lon, lat):
    '''Converts latitude, longitude to column, row in the given dataset.'''

    # Invert the transformation between coordinate systems.
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    target = osr.SpatialReference()
    target.ImportFromWkt(ds.GetProjection())

    transform = osr.CoordinateTransformation(source, target)
    geolon, geolat, _ = transform.TransformPoint(lon, lat)

    x_upper_left, xres, xskew, y_upper_left, yskew, yres = ds.GetGeoTransform()

    # Solve for column and row.
    b = np.array([geolon - x_upper_left, geolat - y_upper_left])
    A = np.array([[xres, xskew], [yskew, yres]])

    x = np.linalg.lstsq(A, b)

    # Returns: col, row.
    return int(x[0][0]), int(x[0][1])


if __name__ == '__main__':

    # Example.
    ds = gdal.Open('MinerStreetSmall.tif')

    lon, lat = pixel_to_coord(ds, ds.RasterXSize, ds.RasterYSize)
    print(f'Raster size (x, y): {ds.RasterXSize}, {ds.RasterYSize}')

    transform = transform_geodetic_to_latlon(ds, lon, lat)
    print(f'With pixel offset: {transform}')

    print(f'Column, row: {coord_to_pixel(ds, transform[0], transform[1])}')
    print('Should be the same as the raster size.')
