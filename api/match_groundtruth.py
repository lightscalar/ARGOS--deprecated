from database import *
from geo_utils import *
from truther import *
from vessel import Vessel

from ipdb import set_trace as debug
import pylab as plt
import os
from tqdm import tqdm


def ground_truth_in_image(truth, image_name):
    """Is this ground truth in this image?"""
    pos = truth["latlon"]
    return in_image(pos, image_name)


class GroundTruthMatcher(object):
    """Automatically find all ground truth objects associated with image."""

    def __init__(self, image_object, truths, truth_tree):
        """Look at all nearby groundtruth candidates."""
        self.image_object = image_object
        self.image_location = image_object["image_loc"]
        self.exif_obj = extract_info(self.image_location)
        self.image_radius = calculate_image_radius_in_meters(self.exif_obj)
        self.tree = truth_tree
        self.truths = truths
        self.location = [[self.exif_obj["img_lat"], self.exif_obj["img_lon"]]]
        self.find_candidates()
        self.find_matches()
        self.insert_matches()

    def find_candidates(self):
        """Find all nearby ground truth candidates."""
        _, self.candidates = self.tree.query(self.location, k=100)

    def find_matches(self):
        """Find candidates contained in the image."""
        present_in_image = []
        for idx in self.candidates[0]:
            dist = distance_on_earth(self.location[0], self.truths[idx]["latlon"])
            if dist < self.image_radius:
                if ground_truth_in_image(self.truths[idx], self.image_location):
                    present_in_image.append(self.truths[idx])
            else:
                print(f"Next ground truth is {dist:.2f} meters away.")
                print(f"Image radius is {self.image_radius} meters.")
                break
        print(
            f"Number of Ground Truth Points Present in Image: {len(present_in_image)}"
        )
        self.present_in_image = present_in_image

    def make_ground_truth_object(self, truth):
        """Create a groundtruth object."""
        plant_data = plant_collection.find_one({"species_codes": truth["species_code"]})
        if plant_data:
            row, col = project_on_image(*truth["latlon"], self.image_location)
            ground_truth = {"scientific_name": plant_data["scientific_name"]}
            ground_truth["species_code"] = plant_data["species_codes"][0]
            ground_truth["position_in_image"] = [row, col]
            return ground_truth
        else:
            return None

    def insert_matches(self):
        """Inserting the matches into the database."""
        self.image_object["ground_truth"] = []
        for truth in self.present_in_image:
            # Add ground truth object to image's ground truth array
            ground_truth = self.make_ground_truth_object(truth)
            if ground_truth:
                self.image_object["ground_truth"].append(ground_truth)
            image_collection.update_one(
                {"_id": self.image_object["_id"]},
                {"$set": self.image_object},
                upsert=False,
            )


if __name__ == "__main__":

    # Get truth from GPS downloads.
    truths = extract_ground_truth()

    # Build a Ball Tree for querying things.
    truth_locations = []
    for truth in truths:
        truth_locations.append(location_from_truth(truth))

    # Get locations.
    truth_locations = np.array(truth_locations)
    tree = BallTree(truth_locations, metric=distance_on_earth)

    all_images = image_collection.find({})
    total_number_of_images = all_images.count()
    itr = 0
    for image in all_images:
        itr += 1
        print(f"{itr}/{total_number_of_images}")
        obj = GroundTruthMatcher(image, tree)

    # drc = "/Users/mjl/Dropbox (Personal)/MAC/DEPOT/MNFI/FLIGHTS/2018.06.21/St. John's Marsh (66)"
    # image_name = "DJI_0155.JPG"
    # image_location = f"{drc}/{image_name}"
    # image_object = image_collection.find_one({"image_loc": image_location})
