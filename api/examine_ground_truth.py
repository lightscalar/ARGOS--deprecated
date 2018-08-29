"""Evaluate the accuracy of ground truthing."""
from database import *
from geo_utils import *
from vessel import Vessel

from glob import glob
from ipdb import set_trace as debug
import pylab as plt
import os
from tqdm import tqdm


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

    plt.ion()
    gt = Vessel("ground_truth.dat")
    thumbnail_locations = "/Users/mjl/Dropbox (Personal)/MAC/DEPOT/MNFI/THUMBNAILS"

    WIDTH = 250
    start = 650

    for itr, truth in enumerate(gt.truths[start:]):
        print(itr + start)
        code = truth["species_code"]
        dirs = glob(f"{thumbnail_locations}/*")
        dirs_ = [os.path.basename(d) for d in dirs]
        if code not in dirs_:
            os.mkdir(f"{thumbnail_locations}/{code}")

        # Extract the latitude and longitude.
        lat, lon = truth["latlon"]

        for idx in range(len(truth["images"])):
            plt.close("all")
            image_number = len(glob(f"{thumbnail_locations}/{code}/*.png")) + 1
            if image_number > 100:
                continue
            img_obj = image_collection.find_one({"_id": truth["images"][idx]})
            img = plt.imread(img_obj["image_loc"].replace("'", ""))
            x, y = project_on_image(lat, lon, img_obj["image_loc"].replace("'", ""))
            subimage = img[
                int(y) - WIDTH : int(y) + WIDTH, int(x) - WIDTH : int(x) + WIDTH, :
            ]

            # Make a picture.
            try:
                filename = f"{thumbnail_locations}/{code}/{image_number:04d}.png"
                print(f"Saving {filename}.")
                borderless_image(subimage)
                # artist.set_data(subimage)
                # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
                # plt.margins(0, 0)
                # ax.xaxis.set_major_locator(plt.NullLocator())
                # ax.yaxis.set_major_locator(plt.NullLocator())
                plt.savefig(filename, bbox_inches="tight")
            except:
                pass
