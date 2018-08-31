'''

    Find the latitude, longitude position of any pixel in a georeferenced tif file.

'''

from osgeo import gdal, osr


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

    nx = (xres * col) + (xskew * row) + x_upper_left
    ny = (yskew * col) + (yres * row) + y_upper_left

    return nx, ny


if __name__ == '__main__':

    # Example.
    ds = gdal.Open('MinerStreetSmall.tif')

    x_upper_left, xres, xskew, y_upper_left, yskew, yres = ds.GetGeoTransform()
    x, y = pixel_to_coord(ds, ds.RasterXSize, ds.RasterYSize)

    print(f'0, 0 transform: {transform_geodetic_to_latlon(ds, x_upper_left, y_upper_left)}')
    print(f'With pixel offset: {transform_geodetic_to_latlon(ds, x, y)}')
