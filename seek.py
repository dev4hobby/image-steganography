import json
import argparse
from binjector.steganography import Steganography
from binjector.utils import read_settings

parser = argparse.ArgumentParser(description='Hide a message in an image.')
parser.add_argument('-in', '--in-image', help='The image to seek message in.', required=False)
args = parser.parse_args()
settings = read_settings()

in_file_name = args.in_image if args.in_image else settings.get("modified_image")

s = Steganography()
# seek your message into image
try:
  print(s.seek_message(in_file_name))
except Exception as e:
  raise e
