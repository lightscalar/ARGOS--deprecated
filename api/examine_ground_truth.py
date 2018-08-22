"""Evaluate the accuracy of ground truthing."""
from database import *
from geo_utils import *
from vessel import Vessel

from glob import glob
import pylab as plt
import os


def borderless_image(image, cmap="hot", fignum=100, filename=None):
    """Make a nice borderless image."""
    plt.figure(fignum)
    plt.imshow(image, cmap=cmap)
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.show()


if __name__ == "__main__":

    target_code = "FA"
    gt = Vessel("ground_truth.dat")
    thumbnail_locations = '/Users/mjl/Dropbox (Personal)/MAC/DEPOT/MNFI/THUMBNAILS'

    targets = []
    # for t in gt.truths:
    #     if t["species_code"] == target_code:
    #         targets.append(t)

    for truth in gt.truths:
        code = truth['species_code']



    tgt = targets[122]
    lat, lon = tgt["latlon"]

    img_obj = image_collection.find_one({"_id": tgt["images"][9]})
    img = plt.imread(img_obj["image_loc"].replace("'", ""))

    x, y = project_on_image(lat, lon, img_obj["image_loc"].replace("'", ""))

    plt.ion()
    plt.close("all")
    plt.imshow(img)
    plt.plot(x, y, "r+", markersize=15)
    plt.plot(x, y, "ro", markersize=8)

    width = 250
    subimage = img[int(y) - width : int(y) + width, int(x) - width : int(x) + width, :]
    borderless_image(subimage)
    plt.savefig('test.png', bbox_inches='tight')

