"""Provide an API endpoint for the QuoteMachine."""
from database import *

from bson import ObjectId
from glob import glob
import eventlet
from eventlet import wsgi
from flask import Flask, request, jsonify, Response, make_response, send_file
from flask_restful import Resource, Api
from flask_cors import CORS
from ipdb import set_trace as debug
import json
import os
from tqdm import tqdm
from skimage.io import imread, imsave
import io


PORT = 2005
app = Flask(__name__)
CORS(app)
api = Api(app)


# Load flight summary data once, at start.
flight_summary = flight_summaries()


class Plants(Resource):
    """Return a wait time quote given the party information."""

    def post(self):
        """Create a new Plant species."""
        plant = request.json
        created = create_plant(plant)

    def get(self):
        """List all current species"""
        plant_list = list_plants()
        return plant_list


class Plant(Resource):
    """Resources for a specific plant."""

    def put(self, plant_id):
        """Update this plant."""
        plant = request.json
        update_plant(plant)
        return plant

    def delete(self, plant_id):
        """Delete this plant."""
        print(plant_id)
        delete_plant(plant_id)


class Images(Resource):
    """Manage all flights/dates."""

    def get(self):
        """List all the available images."""
        return flight_summary


class Image(Resource):
    """Handle individual image information."""

    def get(self, image_id):
        """Return data for the target image."""
        _id = ObjectId(image_id)
        doc = image_collection.find_one({"_id": _id})
        doc["_id"] = str(doc["_id"])
        doc["image_loc"] = doc["image_loc"].replace("'", "")
        return doc


class ImageServer(Resource):
    """Serve requested image."""

    def get(Resource):
        """Return current image."""
        with open("DJI_0206.JPG", "rb") as bites:
            return send_file(io.BytesIO(bites.read()), mimetype="image/jpg")


# ADD RESOURCE ROUTES.
api.add_resource(Plants, "/plants", methods=["POST", "GET"])
api.add_resource(Plant, "/plant/<plant_id>", methods=["PUT", "DELETE"])
api.add_resource(Images, "/images", methods=["GET"])
api.add_resource(Image, "/image/<image_id>", methods=["GET"])
api.add_resource(ImageServer, "/imageserver", methods=["GET"])

if __name__ == "__main__":

    # Launch a WSGI server (more robust than Flask's toy version).
    wsgi.server(eventlet.listen(("localhost", PORT)), app)
