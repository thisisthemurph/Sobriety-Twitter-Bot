import os
import random
import string

from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype("Fonts/Roboto-Black.ttf", size=150)
FONT_COLOR = "rgb(61, 50, 76)"

def get_random_string():
    return "".join(random.choice(string.ascii_letters) for i in range(8))

class Chip:
    """
    A representation of a sobriety chip

    Attributes:
        number (str): The number associated with the Chip
        path (str): The path to the Chips temporary image location
        image_exists (bool): True if the temporary image exists, otherwise False

    Args:
        number (strorint): the number to be placed in the center of the chip

    """
    def __init__(self, number: str or int):
        self.number: str = f"{number}"
        self.path: str = f"Images/temp_{get_random_string()}.png"

        self._make()
    
    def _make(self) -> None:
        """
        Creates the temporaty image at Chip.path
        """
        image = Image.open("Images/sobriety_chip.png")

        draw = ImageDraw.Draw(image)
        w, h = draw.textsize(self.number, font=FONT)
        x, y = (image.size[0] - w) / 2, (image.size[1] - h) / 2 - 10
        draw.text((x, y), self.number, fill=FONT_COLOR, font=FONT)

        image.save(self.path)
    
    def delete(self) -> None:
        """
        Deletes the temporary image
        """
        if os.path.exists(self.path):
            os.remove(self.path)
