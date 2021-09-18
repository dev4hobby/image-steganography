import json
import argparse
from steganography import Steganography

parser = argparse.ArgumentParser(description='Hide a message in an image.')
parser.add_argument('-in', '--in-image', help='The image to hide the message in.', required=False)
parser.add_argument('-out', '--out-image', help='The image to save the message in.', required=False)
parser.add_argument('-m', '--message', help='The message file path to hide.', required=False)
args = parser.parse_args()

with open("settings.json", "r") as setting_file:
  settings = json.load(setting_file)
message_file_name = args.message if args.message else settings.get('payload')
in_file_name = args.in_image if args.in_image else settings.get('in_image')
out_file_name = args.out_image if args.out_image else settings.get('out_image')

s = Steganography()
# hide your message into image
try:
  with open(message_file_name, "r") as message_file:
    message = message_file.read()
  s.hide_message(in_file_name, out_file_name, message)
except Exception as e:
  raise e
