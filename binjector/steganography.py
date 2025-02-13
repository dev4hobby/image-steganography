import io
import logging
from typing import Tuple, Union

import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage

from .utils import get_resized_ratio, get_timestamp_as_md5, read_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class Steganography:
    """
    class for hiding and extracting message on your image
    """

    def __init__(self):
        settings = read_settings()
        self.bits = int(settings.get("bits", 8))
        self.encoding = settings.get("encoding", "utf-8")
        self.token_string = settings.get("token_string", "#secret#")

    def get_pixel_info(self, imarray: np.ndarray) -> np.ndarray:
        return np.array(imarray)

    def get_verified_array(self, shape: Tuple[int, ...]) -> np.ndarray:
        """
        get verified ndarray
        """
        return np.ndarray(shape, dtype=np.uint8)

    def binstr_to_ascii(self, message: str) -> str:  ###
        """
        Convert binary string to ascii string
        """
        byte_list = [message[i : i + 8] for i in range(0, len(message), 8)]
        result = bytes([int(uint8, 2) for uint8 in byte_list]).decode("utf-8")
        return result

    def resize_image(
        self,
        image: PILImage,
        size: Tuple[int, int],
        save=False,
        file_name="resized_image.png",
    ) -> PILImage:
        """
        Resize image to specific size
        """
        image.thumbnail(size, Image.Resampling.LANCZOS)
        if save:
            image.save(file_name)
        return image

    def modify_image_format(self, filename: str, ext: str):
        """
        Modify image format and save as new file
        """
        image = Image.open(filename)
        filename = ".".join(filename.split(".")[:-1])
        image.save(".".join([filename, ext]), ext.upper())

    def save_imarray_as_file(self, imarray: np.ndarray, out_file_name: str) -> None:
        """
        save numpy array as image file
        """
        image = Image.fromarray(imarray)
        image.save(out_file_name)

    def get_binary_message(self, message: str) -> list:
        return [
            bin(char)[2:].zfill(self.bits) for char in message.encode(self.encoding)
        ] + ["0" * self.bits]

    def message_to_binary(
        self, message: Union[bytes, str, int, np.ndarray, np.uint8]
    ) -> str | list:
        """
        Convert your message to a binary things.
        """
        if type(message) == str:
            return "".join(format(ord(char), "08b") for char in message)
        elif type(message) == bytes or type(message) == np.ndarray:
            return [format(i, "08b") for i in message]
        else:
            raise TypeError("Input type not supported")

    def replace_lsb(
        self,
        image_size: Tuple[int, int],
        message: str,
        pixel_info: np.ndarray,
        modified_array: np.ndarray,
    ) -> np.ndarray:
        binary_message_list = self.get_binary_message(message)
        bits_generator = (character for character in "".join(binary_message_list))
        width, height = image_size
        no_more_bits = False

        for row in range(height):
            for col in range(width):
                if no_more_bits:
                    modified_array[row, col] = pixel_info[row, col]
                else:
                    # FIXME: try~except is not good
                    try:
                        r, g, b = pixel_info[row, col]
                        color_list = [r, g, b]
                    except ValueError:
                        r, g, b, a = pixel_info[row, col]
                        color_list = [r, g, b, a]
                    for index, color in enumerate(color_list):
                        if not no_more_bits and (bit := next(bits_generator, None)):
                            binary = bin(color)[2:].zfill(self.bits)
                            color_list[index] = int(binary[:-1] + bit, 2)
                        else:
                            no_more_bits = True
                            color_list_int = [
                                color for color in color_list if type(color) == int
                            ]
                            color_list_hex = [
                                int(color[2:], 16)
                                for color in color_list
                                if type(color) == str
                            ]
                            color_list = color_list_int + color_list_hex
                            break
                    # Ensure color_list has same length as original pixel
                    while len(color_list) < len(pixel_info[row, col]):
                        color_list.append(0)
                    modified_array[row, col] = tuple(
                        color_list[: len(pixel_info[row, col])]
                    )
        return modified_array

    def get_lsb_string(self, imarray: np.ndarray) -> str:
        """
        get LSB until meet secret token
        """
        binary_token = "".join(
            self.message_to_binary(self.token_string)
            if isinstance(self.message_to_binary(self.token_string), list)
            else self.message_to_binary(self.token_string)
        )
        binary_message = []

        for row in imarray:
            for pixel in row:
                binary_pixel = self.message_to_binary(pixel)
                if len(pixel) == 3:  # RGB
                    binary_message.extend(p[-1] for p in binary_pixel[:3])
                else:  # RGBA
                    binary_message.extend(p[-1] for p in binary_pixel[:4])

                # Convert accumulated bits to string and check for token
                current_message = "".join(binary_message)
                token_index = current_message.find(binary_token)
                if token_index != -1:
                    return current_message[:token_index]

        # If token not found, return error message
        result = self.message_to_binary("Cannot found message")
        return "".join(result) if isinstance(result, list) else result

    def hide_message(self, in_file_name: str, out_file_name: str, message: str) -> None:
        """
        Hide your message in your image
        """
        if len(message) == 0:
            raise ValueError("Data is empty !!")
        message += self.token_string
        image = Image.open(in_file_name)
        need_resize, new_size = get_resized_ratio((image.width, image.height), message)
        if need_resize:
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        pixels = self.get_pixel_info(np.array(image))
        modified_array = self.replace_lsb(
            image_size=image.size,
            message=message,
            pixel_info=pixels,
            modified_array=self.get_verified_array(pixels.shape),
        )
        # init image with modified array
        self.save_imarray_as_file(imarray=modified_array, out_file_name=out_file_name)

    def seek_message(self, in_file_name: str) -> str:
        """
        Show your message from your image
        """
        image = Image.open(in_file_name)
        logger.debug(f"Image size: {image.size}")
        imarray = np.array(image)
        logger.debug(f"Image array shape: {imarray.shape}")
        binary_string = self.get_lsb_string(imarray)
        logger.debug(f"Binary string: {binary_string}")
        return self.binstr_to_ascii(binary_string)

    def hide_message_for_web(self, image: bytes, message: str) -> Union[bytes, None]:
        if len(message) == 0:
            return None
        message += self.token_string
        img = Image.open(io.BytesIO(image))
        pixels = self.get_pixel_info(np.array(img))
        modified_array = self.replace_lsb(
            image_size=img.size,
            message=message,
            pixel_info=pixels,
            modified_array=self.get_verified_array(pixels.shape),
        )
        img_result = Image.fromarray(modified_array)
        buffered = io.BytesIO()
        img_result.save(buffered, format="PNG")
        return buffered.getvalue()

    def seek_message_for_web(self, image: bytes) -> Union[str, None]:
        img = Image.open(io.BytesIO(image))
        imarray = np.array(img)
        binary_string = self.get_lsb_string(imarray)
        return self.binstr_to_ascii(binary_string)
