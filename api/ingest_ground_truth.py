"""Ingest ground truth data and insert into image collection."""
from database import *
from geo_utils import *
from vessel import Vessel

from ipdb import set_trace as debug
from tqdm import tqdm


if __name__ == "__main__":

    # Update all images to have annotations and ground truth.
    images = list(image_collection.find({}))
    for image in tqdm(images):
        image['ground_truth'] = []
        image['annotations'] = []
        image_collection.update_one({'_id': image['_id']}, {'$set': image}, upsert=False)

    # Load the ground truth data from the vessel.
    gt = Vessel("ground_truth.dat")

    # For each point, find the image in which it appears, if any.
    for truth in tqdm(gt.truths):

        # What plant are we talking about here?
        plant_data = plant_collection.find_one({"species_codes": truth["species_code"]})

        # If this is not a plant, we don't care.
        if not plant_data:
            continue

        for image_id in truth["images"]:

            # Load the image.
            img_obj = image_collection.find_one({"_id": image_id})

            # Debug the images.
            if "ground_truth" not in img_obj.keys():
                img_obj["ground_truth"] = []

            # Find location of truth point in the image.
            img_loc = img_obj["image_loc"]
            lat, lon = truth["latlon"]
            position = project_on_image(lat, lon, img_loc)
            ground_truth = {"scientific_name": plant_data["scientific_name"]}
            ground_truth["species_code"] = plant_data["species_codes"][0]
            ground_truth["position_in_image"] = list(position)
            ground_truth["color_code"] = plant_data["color_code"]
            img_obj["ground_truth"].append(ground_truth)
            image_collection.update_one(
                {"_id": img_obj["_id"]}, {"$set": img_obj}, upsert=False
            )
