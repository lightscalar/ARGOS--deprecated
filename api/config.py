"""Useful configuration parameters and constants."""
import getpass


# Find the current user.
user = getpass.getuser()

# Determine location of image data based on current user.
if user == 'mjl':
    IMAGE_LOCATION = "/Users/mjl/Dropbox (Personal)/MAC/DEPOT/MNFI/FLIGHTS"
elif user == 'jgc':
    IMAGE_LOCATION = '/Users/jgc/data/FLIGHTS'
