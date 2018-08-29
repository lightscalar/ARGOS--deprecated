"""Launch the ARGOS system."""
from config import *

from pymongo import MongoClient
import os
from time import sleep
from subprocess import Popen
import sys


def mongo_available():
    """Determine if the Mongo server is running."""
    client = MongoClient(serverSelectionTimeoutMS=50)
    try:
        # Can we talk to the Mongo server?
        client.server_info()
        return True
    except:
        # No, we cannot. :(
        return False


if __name__ == "__main__":

    # 1. Launch Mongo.
    if not mongo_available():
        print('> Launching MongoDB.')
        mongo = Popen(["mongod"])
    else:
        mongo = None

    # 2. Launch the API.
    os.chdir(API_LOCATION)
    print("> Launch API.")
    api = Popen(["python", "api.py"])

    # 3. Launch the front-end vue application.
    os.chdir(STATIC_LOCATION)
    print("> Launch Frontend.")
    frontend = Popen(["http-server", '-p', '8080'])

    # 4. Launch the image server.
    os.chdir(IMAGE_SERVER_LOCATION)
    print("> Launch Image Server.")
    image_server = Popen(["http-server", "-p", "2007"])

    try:
        while True:
            sleep(5)
            sys.stdout.flush()
    except KeyboardInterrupt:
        if mongo:
            mongo.kill()
        api.kill()
        frontend.kill()
        image_server.kill()
