from pathlib import Path

import pytest

from binjector import Steganography
from binjector.utils import SETTING_FILE

PLAIN_TEXT = "Hello, World!"
INPUT_FILE = "assets/input.jpeg"
OUTPUT_FILE = "output.png"


@pytest.mark.timeout(5)  # 5 seconds timeout
def test_hide_and_seek():
    s = Steganography()
    assert Path(SETTING_FILE).exists()

    s.hide_message(INPUT_FILE, OUTPUT_FILE, PLAIN_TEXT)
    assert Path(OUTPUT_FILE).exists()

    got_message = s.seek_message(OUTPUT_FILE)
    assert got_message == PLAIN_TEXT
    assert Path(OUTPUT_FILE).unlink() is None
    assert Path(SETTING_FILE).unlink() is None
    assert not Path(SETTING_FILE).exists()
    assert not Path(OUTPUT_FILE).exists()


@pytest.mark.timeout(5)
def test_hide_and_seek_for_web():
    s = Steganography()
    assert Path(SETTING_FILE).exists()

    with open(INPUT_FILE, "rb") as f:
        image = f.read()

    modified_image = s.hide_message_for_web(image, PLAIN_TEXT)
    assert modified_image is not None

    got_message = s.seek_message_for_web(modified_image)
    assert got_message == PLAIN_TEXT
    assert Path(SETTING_FILE).unlink() is None
    assert not Path(SETTING_FILE).exists()
