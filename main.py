import logging
import os
from PIL import Image, ImageFont, ImageDraw, ImageOps
import segno

from ImagePillow.command import add_border_color_to_image


def generate_qrcode(data: str, output_path: str, scale: int = 20, border: int = 2):
    """Generate a QR code and save it as a PNG file."""
    qr = segno.make(data)
    qr.save(output_path, scale=scale, border=border)
    print(f"QR code saved to {output_path}")


def add_logo_to_qrcode(
    qr_path: str,
    logo_path: str,
    output_path: str,
    logo_size: tuple = (200, 200),
    border_size_ratio: float = 0.05,
):
    """Add a logo to the center of the QR code with a border."""
    qr_img = Image.open(qr_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    # Resize logo
    logo = logo.resize(logo_size)

    # Create circle mask
    circle_mask = Image.new("L", logo_size, 0)
    draw = ImageDraw.Draw(circle_mask)
    draw.ellipse((0, 0, logo_size[0], logo_size[1]), fill=255)
    circle_mask.putalpha(circle_mask.point(lambda x: 0 if x < 150 else 255))

    # Overlay the logo on the QR code
    qr_img.paste(
        logo,
        (
            qr_img.size[0] // 2 - logo_size[0] // 2,
            qr_img.size[1] // 2 - logo_size[1] // 2,
        ),
        mask=circle_mask,
    )

    # Calculate border size based on logo size
    border_size = int(min(logo_size) * border_size_ratio)

    # Draw border around the logo
    draw = ImageDraw.Draw(qr_img)
    draw.ellipse(
        (
            qr_img.size[0] // 2 - logo_size[0] // 2 - border_size,
            qr_img.size[1] // 2 - logo_size[1] // 2 - border_size,
            qr_img.size[0] // 2 + logo_size[0] // 2 + border_size,
            qr_img.size[1] // 2 + logo_size[1] // 2 + border_size,
        ),
        outline=(0, 0, 0),
        width=border_size,  # Adjust the width as needed
    )

    qr_img.save(output_path)
    print(f"QR code with logo and border saved to {output_path}")


def add_text_to_below_qrcode(
    text: str, qr_path: str, output_path: str, font_size: int = 95
):
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    qr_img = Image.open(qr_path).convert("RGBA")

    text_width, text_height = font.getbbox(text)[2:]
    qr_width, qr_height = qr_img.size
    new_image_height = qr_height + text_height + font_size

    # Create a new blank image for QR + text
    new_image = Image.new("RGB", (qr_width, new_image_height), "black")
    new_image.paste(qr_img, (0, 0))

    # Draw text
    draw = ImageDraw.Draw(new_image)
    text_position = ((qr_width - text_width) // 2, qr_height + (font_size // 2))
    draw.text(text_position, text, fill="white", font=font)

    # Save final image
    new_image.save(output_path)
    print(f"QR code with text below saved to {output_path}")


def add_rounded_corners(qr_path: str, output_path: str, radius: float = 20):
    """Applies rounded corners to an image."""
    qr_img = Image.open(qr_path).convert("RGBA")
    mask = Image.new("L", qr_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, *qr_img.size), radius=radius, fill=255)

    rounded_img = Image.new("RGBA", qr_img.size)
    rounded_img.paste(qr_img, (0, 0), mask=mask)
    rounded_img.save(output_path)
    print(f"QR code with rounded corners saved to {output_path}")


def main():
    data = "https://uam.online.com.kh/.well-known/deep.html?id=2380"
    pre_file_name = "pre_file.png"
    result_file_name = "result.png"

    is_add_logo = (
        input("Do you want to add logo to QrCode? (Yes/No): ").strip().lower() == "yes"
    )
    logo_path = input("Please input logo path: ") if is_add_logo else None
    is_add_text = (
        input("Do you want to add text below the QR code? (Yes/No): ").strip().lower()
        == "yes"
    )
    below_text = input("Please input the text: ") if is_add_text else None
    is_add_radius = (
        input("Do you want to add radius to QrCode? (Yes/No): ").strip().lower()
        == "yes"
    )
    radius = int(input("Please input radius: ") or 20) if is_add_radius else 20

    if is_add_logo and not logo_path:
        print("Logo path must be provided if 'is_add_logo' is Yes/Y/y.")
        return
    elif is_add_logo and not os.path.exists(logo_path):
        print(f"Logo path '{logo_path}' does not exist.")
        return

    try:
        generate_qrcode(data, pre_file_name)

        if is_add_logo:
            add_logo_to_qrcode(pre_file_name, logo_path, result_file_name)
            os.remove(pre_file_name)
        else:
            os.rename(pre_file_name, result_file_name)

        if is_add_text:
            os.rename(result_file_name, pre_file_name)
            add_text_to_below_qrcode(
                text=below_text, qr_path=pre_file_name, output_path=result_file_name
            )
            os.remove(pre_file_name)

        if is_add_radius:
            os.rename(result_file_name, pre_file_name)
            add_rounded_corners(
                qr_path=pre_file_name, output_path=result_file_name, radius=radius
            )
            os.remove(pre_file_name)

        print("Done!")
        # Uncomment the following line to open the result file automatically
        # os.startfile(result_file_name)

    except Exception as e:
        logging.exception("An error occurred: %s", e)


if __name__ == "__main__":
    main()
    add_border_color_to_image(
        image_path="result.png",
        output_path="output.png",
        border_size=20,
        border_radius=20,
        color=(0, 0, 0),
    )
