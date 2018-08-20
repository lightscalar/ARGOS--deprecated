"""Utilities for working with geo-rectified imagery."""
from exiftool import ExifTool
import numpy as np


# Define necessary constants.
meters_per_degree = 111.111e3


def calculate_meters_per_pixel(fov, altitude, diagonal_length):
    """Compute meters_per_pixel for the image."""
    fov_over_2 = fov / 2 * np.pi / 180
    diag_over_2 = diagonal_length / 2
    half_diag_in_meters = altitude * np.tan(fov_over_2)
    half_diag_in_pixels = diagonal_length / 2
    return half_diag_in_meters / half_diag_in_pixels


def unit_vectors(camera_yaw):
    """Compute east and north unit vectors given the camera yaw."""
    alpha = -camera_yaw * np.pi / 180
    n = [np.sin(alpha), np.cos(alpha)]
    e = [np.cos(alpha), -np.sin(alpha)]
    return np.array(n), np.array(e)


def extract_info(image_file):
    """Extract necessary data from metadata dictionary."""
    with ExifTool() as et:
        metadata = et.get_metadata(image_file)
    data = {}
    data["field_of_view"] = metadata["Composite:FOV"]
    data["camera_yaw"] = metadata["MakerNotes:CameraYaw"]
    data["relative_altitude"] = float(metadata["XMP:RelativeAltitude"])
    data["img_lat"] = metadata["Composite:GPSLatitude"]
    data["img_lon"] = metadata["Composite:GPSLongitude"]
    data["img_width"] = metadata["File:ImageWidth"]
    data["img_height"] = metadata["File:ImageHeight"]
    return data


def project_on_image(lat, lon, image_file):
    """Project given lat and lon onto coordinate system of the specified image."""
    d = extract_info(image_file)
    diagonal_length_in_pixels = np.sqrt(d["img_width"] ** 2 + d["img_height"] ** 2)
    meters_per_pixel = calculate_meters_per_pixel(
        d["field_of_view"], d["relative_altitude"], diagonal_length_in_pixels
    )
    # Compute the unit vectors in the north and east directions.
    # Find dispacement in those directions, given specfied latitude/longitude.
    n, e = unit_vectors(d["camera_yaw"])
    dn_in_meters = (lat - d["img_lat"]) * meters_per_degree
    de_in_meters = (
        (lon - d["img_lon"]) * np.cos(d["img_lat"] * np.pi / 180) * meters_per_degree
    )
    # Compute delta in N/S and E/W direction.
    dn_in_pixels = dn_in_meters / meters_per_pixel
    de_in_pixels = de_in_meters / meters_per_pixel

    # Projected position is location relative to center of image.
    ctr_position = np.array([d["img_width"] / 2, d["img_height"] / 2])
    target_position = ctr_position + (dn_in_pixels * n + de_in_pixels * e)
    return target_position


def is_it_in_image(lat: float, lon: float, image_file: str):
    """Determine if a latitude/longitude coordinate is contained within specified image."""
    target_position = project_on_image(lat, lon, image_file)
    lat_bounds = (target_position[0] > 0) * (target_position[0] < 4000)
    lon_bounds = (target_position[1] > 0) * (target_position[1] < 3000)
    return lat_bounds * lon_bounds


if __name__ == "__main__":

    # Example.
    import pylab as plt

    img_file = "DJI_0206.JPG"
    img = plt.imread(img_file)
    data = extract_info(img_file)
    lat = data["img_lat"]
    lon = data["img_lon"]

    plt.ion()
    plt.close("all")
    plt.imshow(img)
    point = project_on_image(lat+11e-5, lon, img_file)

    plt.plot(point[0], point[1], "r+", markersize=22)
    plt.plot(point[0], point[1], "ro", markersize=8)
