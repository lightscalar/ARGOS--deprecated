"""Utilities for accessing the database, grabbing data, etc."""
from config import *

from bson import ObjectId
from exiftool import ExifTool
from pymongo import MongoClient

# Open up a database instance.
client = MongoClient()

# Connect to the database.
db = client.ARGOS  # database

# Define our collections.
plant_collection = db.plants
annotations_collection = db.annotations
flight_collection = db.flights
image_collection = db.images


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
