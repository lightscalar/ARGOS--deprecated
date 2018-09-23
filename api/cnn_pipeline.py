"""Process annotation/image data for CNN training."""
from database import *
from vessel import Vessel


# Find all images that have been annotated.
annotated_images = image_collection.find({'$where': 'this.annotations.length>0'})

