"""Manage image collections for ARGOS."""
from config import *

from glob import glob
import h5py
import os
from ipdb import set_trace as debug
import re


class ImageManager(object):
    """Manage all the imagery data for the ARGOS project."""

    def __init__(self, hd5_filename="images.hdf5"):
        """Ingest available flight data into HDF5 file."""
        self.hd5_filename = hd5_filename

        # Find all available flight_dates.
        self.flight_dates = flight_dates = glob(f"{IMAGE_LOCATION}/*")

        # Find all dates of data collection.
        self.flights = flights = {}
        for flight_date in self.flight_dates:
            # Find all the sites flown on this date.
            the_date = os.path.basename(flight_date)
            flights = glob(f"{flight_date}/*")
            self.flights[the_date] = {}
            for site in flights:
                # Find all the images associated with this site.
                base_site = os.path.basename(site)
                image_list = glob(f"{flight_date}/{base_site}/*.JPG")
                self.flights[the_date][base_site] = image_list

        # Ingest all imagery into HDF5 file.
        self.ingest_imagery()

    def ingest_imagery(self):
        """Given available flights, ingest imagery data into HDF5 file."""
        self.store = h5py.File(self.hd5_filename, "w")

        # Loop through the dates/sites/images and insert them into the
        # database. Also extract the metadata from all the images, too, via
        # exiftool, etc. Add this information to the attrs, as appropriate.

