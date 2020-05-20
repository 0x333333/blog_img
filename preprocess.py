from PIL import Image
from PIL import ExifTags
from PIL import ImageDraw
from PIL import ImageFont
import os
import argparse

parser = argparse.ArgumentParser(description='Arguments for pre processor.')
parser.add_argument("--t", default="zpjiang.me", help="Default value for water mark.")
parser.add_argument("--w", type=int, default=130, help="The num of pixels for the water mark.")
args = parser.parse_args()

# The base width of images.
BASE_WIDTH = 1024
WATERMARK = "zpjiang.me"


# Decide whether to proceed with rotation, shrinking or not.
def _should_proceed(image_path):
    return ('jpg' in filepath or
            'JPG' in filepath or
            'jpeg' in filepath or
            'JPEG' in filepath or
            'png' in filepath or
            'PNG' in filepath)


# Rotates image if needed.
def _rotate(image):
    if not image:
        return

    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass

    return image


# Shrinks image if needed.
def _shrink(image):
    if not image:
        return

    width = float(image.size[0])
    height = float(image.size[1])
    if width > BASE_WIDTH:
        ratio = BASE_WIDTH / width
        width = BASE_WIDTH
        height = int(height * ratio)
        image = image.resize((width, height), Image.ANTIALIAS)

    return image


# Adds watermark.
def _watermark(image, text='zpjiang.me', w=130):
    if not image:
        return

    # make the image editable
    drawing = ImageDraw.Draw(image)

    # find the position
    width = image.size[0]
    height = image.size[1]
    pos = (width - w, height - 35)

    white = (255, 255, 255)
    font = ImageFont.truetype("Arial.ttf", 20)
    drawing.text(pos, text, fill=white, font=font)


if __name__ == '__main__':
    arr = os.listdir('.')
    for filepath in arr:
        if _should_proceed(filepath):
            print ("start: " + filepath)
            image = Image.open(filepath)
            image = _rotate(image)
            image = _shrink(image)
            _watermark(image, args.t, args.w)
            image.save("../z_" + filepath)
            print ("saved: ../z_" + filepath)
