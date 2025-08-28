import os

from PIL import Image


def img_to_webp():
    img_dir = os.path.join("static", "images")
    for filename in os.listdir(img_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(img_dir, filename)
            with Image.open(img_path) as img:
                webp_path = os.path.splitext(img_path)[0] + '.webp'
                img.save(webp_path, 'WEBP', quality=85)
