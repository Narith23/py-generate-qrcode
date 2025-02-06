import logging
import os
from PIL import Image, ImageDraw
import segno


def generate_qrcode(
    is_add_logo: bool = False,
    logo_path: str = None,
):
    try:
        print("In Function")
        if is_add_logo and logo_path is None:
            print("Logo path must be provided if 'is_add_logo' is Yes/Y/y.")
            return
        elif is_add_logo and not os.path.exists(logo_path):
            print(f"Logo path '{logo_path}' does not exist.")
            return
        else:
            print("Else")

    except Exception as e:
        logging.exception(str(e))
    # # QR Data (Replace with actual payment or website link)
    # data = "https://example.com"
    # pre_file_name = "pre_file.png"

    # print("================================================================")
    # print("Step 1: Generate the QR code using Segno")
    # print("================================================================")
    # print("")
    # # Generate QR Code with `segno`
    # qr = segno.make(data)
    # # Save QR Code as PNG
    # qr_path = pre_file_name
    # qr.save(qr_path, scale=15, border=2)
    # print("Done!")
    # print("")

    # print("================================================================")
    # print("Step 2: Add logo to QrCode file")
    # print("================================================================")
    # print("")
    # # Open QR Code
    # qr_img = Image.open(qr_path).convert("RGBA")

    # # Load and Process the Logo
    # logo = Image.open(logo_path).convert("RGBA")

    # # Resize Logo (Adjust size based on QR Code)
    # logo_size = qr_img.size[0] // 5  # Pre logos are usually smaller
    # logo = logo.resize((logo_size, logo_size))

    # # Create White Background for Logo (To ensure readability)
    # border_size = 10  # Padding around the logo
    # logo_bg_size = (logo_size + 2 * border_size, logo_size + 2 * border_size)

    # # Create a white background image
    # logo_bg = Image.new("RGBA", logo_bg_size, (255, 255, 255, 255))

    # # Paste the logo onto the white background
    # logo_bg.paste(logo, (border_size, border_size), mask=logo)

    # # Calculate Logo Position (Centered)
    # pos = (
    #     (qr_img.size[0] - logo_bg_size[0]) // 2,
    #     (qr_img.size[1] - logo_bg_size[1]) // 2,
    # )

    # # Overlay the Logo on the QR Code
    # qr_img.paste(logo_bg, pos, mask=logo_bg)

    # # Save the Final KHQR-Style QR Code
    # qr_img.save("result.png")

    # print("Done!")
    # print("")

    # print("================================================================")
    # print("Step 3: Remove pre file")
    # print("================================================================")
    # print("")
    # # Remove pre file
    # os.remove(pre_file_name)
    # print("Done!")
    # print("")


def add_rounded_corners(img, radius):
    """Applies rounded corners to an image."""
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, *img.size), radius=radius, fill=255)

    rounded_img = img.convert("RGBA")
    rounded_img.putalpha(mask)

    return rounded_img


if __name__ == "__main__":
    is_add_logo = (
        input("Do you want to add logo to QrCode? (Yes/No): ").strip().lower() == "yes"
    )
    is_add_logo = False
    if is_add_logo == "yes" or is_add_logo == "y" or is_add_logo == "Y":
        is_add_logo = True
    logo_path = input("Please input logo path: ")

    generate_qrcode(logo_path=logo_path, is_add_logo=is_add_logo)
