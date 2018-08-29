"""Utilities for accessing the database, grabbing data, etc."""
from config import *

from bson import ObjectId
from datetime import datetime
from exiftool import ExifTool
from ipdb import set_trace as debug
import numpy as np
import pymongo
from pymongo import MongoClient
import os
import re

# Open up a database instance.
client = MongoClient()

# Connect to the database.
db = client.ARGOS  # database

# Define our collections.
plant_collection = db.plants
annotations_collection = db.annotations
flight_collection = db.flights
image_collection = db.images


def get_image(image_id):
    """Return the image object corresponding to the image id."""
    return image_collection.find_one({"_id": image_id})


def update_image(image):
    """Update existing image in Mongo database."""
    _id = {"_id": ObjectId(image["_id"])}
    del image["_id"]
    image_collection.update_one(_id, {"$set": image}, upsert=False)


def create_plant(plant):
    """Insert a new species into the database."""
    plant = plant_collection.insert_one(plant)
    return plant


def update_plant(plant):
    """Update existing plant species."""
    _id = {"_id": ObjectId(plant["_id"])}
    del plant["_id"]
    plant_collection.update_one(_id, {"$set": plant}, upsert=False)


def delete_plant(plant_id):
    """Delete the specified plant from database."""
    _id = {"_id": ObjectId(plant_id)}
    plant_collection.delete_one(_id)


def list_plants():
    """List all species in the database."""
    plant_list = list(plant_collection.find({}))
    # ObjectId is not serializable, so...
    for plant in plant_list:
        plant["_id"] = str(plant["_id"])
    return plant_list


def create_image_doc(date, flight_name, image_loc):
    """Add a new image to the database"""
    with ExifTool() as et:
        metadata = et.get_metadata(image_loc)
    image_doc = {
        "date": date,
        "flight_name": flight_name,
        "image_loc": image_loc,
        "metadata": metadata,
        "annotated": False,
    }
    return image_doc


def flight_summaries():
    """Returns abbreviated flight summaries — just the facts, ma'am."""

    # Define a date regex.
    ymd = r"(\d+).(\d+).(\d+)"
    available_dates = np.array(image_collection.distinct("date", {}))
    available_dates_ = []
    idx = np.argsort(available_dates)
    available_dates = available_dates[idx]
    available_dates_ = []
    data = []

    # Loop over dates of data collection.
    for date in available_dates:
        on_this_day = {}
        m = re.search(ymd, date)
        date_ = datetime(int(m[1]), int(m[2]), int(m[3])).strftime("%B %d, %Y")
        on_this_day["date"] = date_
        on_this_day["flights"] = []
        flights = image_collection.distinct("flight_name", {"date": date})

        # Loop over flights on those dates.
        for flight in flights:
            this_flight = {"flight_name": flight}
            flight_images = list(
                image_collection.find(
                    {"date": date, "flight_name": flight}, {"image_loc": 1}
                )
            )
            for img in flight_images:
                img["_id"] = str(img["_id"])
                img["image_loc_short"] = os.path.basename(img["image_loc"])
            this_flight["images"] = sorted(
                flight_images, key=lambda x: x["image_loc_short"]
            )
            on_this_day["flights"].append(this_flight)
        data.append(on_this_day)
    return data
