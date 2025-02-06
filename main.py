import logging
import os
from PIL import Image, ImageDraw
import segno


def generate_qrcode(data: str, output_path: str, scale: int = 15, border: int = 2):
    """Generate a QR code and save it as a PNG file."""
    qr = segno.make(data)
    qr.save(output_path, scale=scale, border=border)
    print(f"QR code saved to {output_path}")


def add_logo_to_qrcode(
    qr_path: str,
    logo_path: str,
    output_path: str,
    logo_size_ratio: float = 0.2,
    border_size: int = 10,
):
    """Add a logo to the center of the QR code."""
    qr_img = Image.open(qr_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    # Resize logo
    logo_size = int(qr_img.size[0] * logo_size_ratio)
    logo = logo.resize((logo_size, logo_size))

    # Create white background for logo
    logo_bg_size = (logo_size + 2 * border_size, logo_size + 2 * border_size)
    logo_bg = Image.new("RGBA", logo_bg_size, (255, 255, 255, 255))
    logo_bg.paste(logo, (border_size, border_size), mask=logo)

    # Calculate logo position
    pos = (
        (qr_img.size[0] - logo_bg_size[0]) // 2,
        (qr_img.size[1] - logo_bg_size[1]) // 2,
    )

    # Overlay the logo on the QR code
    qr_img.paste(logo_bg, pos, mask=logo_bg)
    qr_img.save(output_path)
    print(f"QR code with logo saved to {output_path}")


def main():
    data = "https://example.com"
    pre_file_name = "pre_file.png"
    result_file_name = "result.png"

    is_add_logo = (
        input("Do you want to add logo to QrCode? (Yes/No): ").strip().lower() == "yes"
    )
    logo_path = input("Please input logo path: ") if is_add_logo else None

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
            print(f"Temporary file {pre_file_name} removed.")
        else:
            os.rename(pre_file_name, result_file_name)

        print(f"Done!")

    except Exception as e:
        logging.exception(str(e))


if __name__ == "__main__":
    main()
