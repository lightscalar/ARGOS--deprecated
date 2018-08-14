from exiftool import ExifTool


img = "DJI_0063.JPG"

with ExifTool() as et:
    metadata = et.get_metadata(img)
