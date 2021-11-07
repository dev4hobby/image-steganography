import json
from math import ceil
from typing import Tuple
from hashlib import md5
from datetime import datetime

def get_timestamp_as_md5():
    return md5(str(datetime.now()).encode('utf-8')).hexdigest()

def create_settings():
    settings = {
        "encoding": "utf8",
        "bits": 8,
        "token_string": get_timestamp_as_md5(),
        "message": "./message.txt",
        "in_image": "./input.png",
        "out_image": "./output.png",
        "modified_image": "./output.png"
    }
    with open("./settings.json", "w") as setting_file:
        json.dump(settings, setting_file)

def read_settings() -> dict:
    try:
        with open("settings.json", "r") as setting_file:
            settings = json.load(setting_file)
        return settings
    except FileNotFoundError:
        create_settings()
        return read_settings()

def set_token():
    settings = read_settings()
    settings['token'] = get_timestamp_as_md5()
    with open("./settings.json", "w") as setting_file:
        json.dump(settings, setting_file)
    print ("Token set to: " + settings['token'])

def message_to_binary(message: str) -> str:
        """
        Convert your message to a binary things.
        """
        return ''.join(format(ord(char), '08b') for char in message)

def get_resized_ratio(image_size: Tuple[int, int], message: str) -> Tuple[bool, Tuple[int, int]]:
    '''
    if need resize, return (True, new size)
    if not need resize, return (False, None)
    '''
    colors = 3
    width, height = image_size
    message_length = len(message_to_binary(message))
    ratio = 1.0
    while ceil(width*ratio) * ceil(height*ratio) * colors < message_length:
        ratio += 0.5
    if ratio > 1.0:
        return (True, (ceil(width*ratio), ceil(height*ratio)))
    return (False, (width, height))
