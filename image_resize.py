import argparse
import os
from PIL import Image


def resize_and_crop_image(input_path, output_path, target_size):
    with Image.open(input_path) as img:
        img.thumbnail((target_size[0], target_size[1]), Image.ANTIALIAS)
        width, height = img.size

        # Calculate cropping dimensions
        left = (width - target_size[0]) / 2
        top = (height - target_size[1]) / 2
        right = (width + target_size[0]) / 2
        bottom = (height + target_size[1]) / 2

        # Crop and save the image
        img_cropped = img.crop((left, top, right, bottom))
        img_cropped.save(output_path)

def process_images(input_dir, output_dir, target_size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            resize_and_crop_image(input_path, output_path, target_size)
            print(str("Processing" + " " + filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image resizing and cropping script")
    parser.add_argument("input_dir", help="Input directory containing images")
    parser.add_argument("resolution", help="Target resolution in format WIDTHxHEIGHT, e.g., 800x480")
    args = parser.parse_args()

    target_width, target_height = map(int, args.resolution.split('x'))
    target_size = (target_width, target_height)

    output_dir = os.path.join(args.input_dir, 'processed')
    process_images(args.input_dir, output_dir, target_size)
