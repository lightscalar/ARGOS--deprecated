"""Utilities for getting at ground truth GPS information."""
from database import *
from geo_utils import *
from vessel import Vessel

from ipdb import set_trace as debug
import fiona
from geopy.distance import distance
import numpy as np
import re
import pandas as pd
import seaborn as sns
from sklearn.neighbors import BallTree
from tqdm import tqdm


# Define regular expression for extracting species code.
REG_EXP = r"(\w+)\s.*"

# Colors.
np.random.seed(0)
colors = list(sns.xkcd_rgb.keys())
np.random.shuffle(colors)


def extract_ground_truth(shape_file="ground_truth/CZM_UAV_WAYPOINTS_2018.shp"):
    """Extract information from the shape files."""
    shapes = fiona.open(shape_file)
    shapes = list(shapes)
    truths = []
    for shape in shapes:
        truth = {}
        truth["geolocation"] = shape["geometry"]["coordinates"]
        truth["latlon"] = (
            shape["geometry"]["coordinates"][1],
            shape["geometry"]["coordinates"][0],
        )
        truth["name"] = shape["properties"]["Name"]
        truth["species_code"] = re.search(REG_EXP, truth["name"])[1]
        truth["symbol"] = shape["properties"]["Symbol"]
        truth["datetime"] = shape["properties"]["DateTimeS"]
        truths.append(truth)
    return truths


def location_from_image(img):
    """Extract GPS coordinates from the image metadata."""
    return (
        img["metadata"]["Composite:GPSLatitude"],
        img["metadata"]["Composite:GPSLongitude"],
    )


def location_from_truth(truth):
    """Extract geolocation from ground truth measurement."""
    return truth["latlon"]


def find_all_images(tree, imgs, truth_locations, truths):
    """Find all images that contain each ground truth location."""
    v = Vessel("ground_truth.dat")
    for idx, truth in tqdm(enumerate(truths)):
        loc = [truth_locations[idx, :]]
        truth["images"] = []
        _, candidates = tree.query(loc, k=100)
        for candidate in candidates[0]:
            if in_image(loc[0], imgs[candidate]["image_loc"]):
                truth["images"].append(imgs[candidate]["_id"])
            else:
                v.truths = truths
                v.save()
                break


if __name__ == "__main__":

    # Load the GPS key.
    gps_key = pd.read_excel("ground_truth/GPS_KEY_08_11_2018.xlsx")
    unique_species = np.unique(list(gps_key["Scientific Name"]))
    plants = []
    for scientific_name in unique_species:
        if scientific_name != "nan":
            plant = {}
            plant["scientific_name"] = scientific_name
            plant["species_codes"] = set([])
            for idx, name in enumerate(gps_key["Scientific Name"]):
                if name == scientific_name:
                    plant["common_name"] = gps_key["Common Name"][idx]
                    plant["physiognomy"] = gps_key["PHYSIOGNOMY"][idx]
                    plant["category"] = gps_key["CATEGORY"][idx]
                    plant["color_code"] = sns.xkcd_rgb[colors[idx]]
                    codes = gps_key["Code"][idx].split(" ")
                    for code in codes:
                        plant["species_codes"].add(code)
            plants.append(plant)
        else:
            continue

    # Get rid of sets.
    for plant in plants:
        plant["species_codes"] = list(plant["species_codes"])

    # Add plants to the database.
    plant_collection.delete_many({})
    plant_collection.insert_many(plants)
