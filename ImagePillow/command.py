from PIL import Image, ImageOps, ImageDraw
import logging


def add_border_color_to_image(
    image_path: str,
    output_path: str,
    border_size: int = 2,
    border_radius: int = 20,
    color: tuple = (0, 0, 0),
):
    """Add a border color to an image and save to a new file."""
    try:
        with Image.open(image_path) as image:
            image_with_border = ImageOps.expand(image, border=border_size, fill=color)
            mask = Image.new("L", image_with_border.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle(
                (0, 0, *image_with_border.size), radius=border_radius, fill=255
            )
            image_with_border.putalpha(mask)
            image_with_border.save(output_path)
        print(f"Border color added to image and saved to {output_path}")
    except Exception as e:
        logging.error(f"Error adding border color to image: {e}")


if __name__ == "__main__":
    image_path = input("Please input image path: ").strip() or "result.png"
    output_path = input("Please input output path: ").strip() or "output.png"
    border_size = int(input("Please input border size: ").strip() or 20)
    radius = int(input("Please input radius: ").strip() or 20)
    color_input = input("Please input border color (RGB): ").strip() or "0,0,0"
    color = tuple(map(int, color_input.split(",")))
    add_border_color_to_image(image_path, output_path, border_size, radius, color)
