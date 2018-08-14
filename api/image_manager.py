"""Manage image collections for ARGOS."""
from config import *
from database import *

from glob import glob
import os
from ipdb import set_trace as debug
import re
from tqdm import tqdm


if __name__ == "__main__":
    """Ingest available flight data into the MONGO DB."""

    # Delete all images.
    image_collection.delete_many({})

    # Find all available flight_dates.
    flight_dates = glob(f"{IMAGE_LOCATION}/*")

    # Find all dates of data collection.
    flights = {}

    for flight_date in tqdm(flight_dates):
        # Find all the sites flown on this date.
        the_date = os.path.basename(flight_date)
        flight_list = glob(f"{flight_date}/*")
        flights[the_date] = {}
        for site in flight_list:
            # Find all the images associated with this site.
            base_site = os.path.basename(site)
            image_list = glob(f"{flight_date}/{base_site}/*.JPG")
            flights[the_date][base_site] = image_list

            # Create an augmented document for each image.
            docs = []
            for img_loc in tqdm(image_list):
                doc = create_image_doc(the_date, base_site, img_loc)
                docs.append(doc)

            # Drop those documents into the MongoDB.
            if len(docs) > 0:
                image_collection.insert_many(docs)
