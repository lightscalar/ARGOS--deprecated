from database import *
from geo_utils import *
from truther import *
from vessel import Vessel

import pylab as plt
import os
from tqdm import tqdm


def ground_truth_in_image(truth, image_name):
    """Is this ground truth in this image?"""
    pos = truth["latlon"]
    return in_image(pos, image_name)


class GroundTruthMatcher(object):
    """Automatically find all ground truth objects associated with image."""

    def __init__(image_location, truth_tree):
        exif_obj = extract_info(image_location)


if __name__ == "__main__":

    truths = extract_ground_truth()
    images = image_collection.find(
        {},
        {
            "metadata.Composite:GPSLatitude": 1,
            "metadata.Composite:GPSLongitude": 1,
            "image_loc": 1,
        },
    )

    # Build a Ball Tree for querying things.
    image_locations = []
    truth_locations = []
    for img in images:
        image_locations.append(location_from_image(img))

    for truth in truths:
        truth_locations.append(location_from_truth(truth))

    # Get locations.
    image_locations = np.array(image_locations)
    truth_locations = np.array(truth_locations)
    tree = BallTree(truth_locations)

    drc = "/Users/mjl/Dropbox (Personal)/MAC/DEPOT/MNFI/FLIGHTS/2018.06.21/St. Johns Marsh (66)"
    image_name = "DJI_0155.JPG"
    image_location = f"{drc}/{image_name}"
    d = extract_info(image_location)
    loc = [[d["img_lat"], d["img_lon"]]]
    image_radius = calculate_image_radius_in_meters(d)

    _, candidates = tree.query(loc, k=25)

    present_in_image = []
    for idx in candidates[0]:
        dist = distance_on_earth(loc, truths[idx]["latlon"])
        if dist < image_radius:
            if ground_truth_in_image(truths[idx], image_location):
                present_in_image.append(truths[idx])
        else:
            print(f"Nearest ground truth is {dist:.2f} meters away.")
            print(f"Image radius is {image_radius} meters.")
            break

    # # image_id = g["images"][2]
    # # image_obj = get_image(image_id)
    # # image_file = image_obj["image_loc"].replace("'", "")
    image_array = plt.imread(image_location.replace("'", ""))

    plt.ion()
    plt.close("all")
    plt.imshow(image_array)

    for g in present_in_image:
        row, col = project_on_image(*g["latlon"], image_location)
        if g["species_code"] == "PA":
            plt.plot(col, row, "r+", markersize=15, label=g["species_code"])
        else:
            plt.plot(col, row, "b+", markersize=15, label=g["species_code"])

    n, e = unit_vectors(d)
    row_ctr = image_array.shape[0] / 2
    col_ctr = image_array.shape[1] / 2
    ctr = np.array([row_ctr, col_ctr])
    north = ctr + 500 * n
    east = ctr + 500 * e

    plt.plot([ctr[1], north[1]], [ctr[0], north[0]], "b-", linewidth=2, label="North")
    plt.plot([ctr[1], east[1]], [ctr[0], east[0]], "r-", linewidth=2, label="East")
    plt.legend()
