"""Launch the ARGOS system."""
from subprocess import Popen
from pymongo import MongoClient
from time import sleep


def mongo_available():
    '''Determine if the Mongo server is running.'''
    client = MongoClient(serverSelectionTimeoutMS=50)
    try:
        # Can we talk to the Mongo server?
        client.server_info()
        return True
    except:
        # No, we cannot. :(
        return False


if __name__ == "__main__":

    counter = 0
    while counter < 5:
        print('Working...')
        sleep(1)
        counter += 1

