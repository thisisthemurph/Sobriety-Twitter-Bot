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
        days (int): The number of days associated with the chip
        number (str): The number associated with the Chip
        path (str): The path to the Chips temporary image location

    Args:
        days (strorint): the number to be placed in the center of the chip

    """
    def __init__(self, days: str or int):
        self.days: int = int(days)
        self.number: str = f"{days}"
        self.path: str = f"Images/temp_{get_random_string()}.png"

        self._make()
    
    def _make(self) -> None:
        """
        Creates a temporary image to be used
        """
        if (self.days <= 365):
            image = Image.open(self._get_premade_image())
        else:
            image = Image.open("Images/sobriety_chip.png")
            draw = ImageDraw.Draw(image)
            w, h = draw.textsize(self.number, font=FONT)
            x, y = (image.size[0] - w) / 2, (image.size[1] - h) / 2 - 10
            draw.text((x, y), self.number, fill=FONT_COLOR, font=FONT)

        image.save(self.path)

    def _get_premade_image(self):
        """
        Returns the path to the appropriate chip image, based on the number of days
        """
        keep = None
        for image in os.listdir("Images/Chips"):
            image_days = int(image.split("-")[1].replace(".png", ""))
            
            if image_days > self.days:
                continue

            if keep == None or image_days > keep:
                keep = image_days
        
        return os.path.join("Images/Chips", f"Chip-{keep}.png")
    
    def delete(self) -> None:
        """
        Deletes the temporary image
        """
        if os.path.exists(self.path):
            os.remove(self.path)
