from PIL import Image
import segno


def generate_khqr(logo_path: str):
    # QR Data (Replace with actual payment or website link)
    data = "https://example.com"

    # Generate QR Code with `segno`
    qr = segno.make(data)

    # Save QR Code as PNG
    qr_path = "pre_qrcode.png"
    qr.save(qr_path, scale=15, border=2)

    # Open QR Code
    qr_img = Image.open(qr_path).convert("RGBA")

    # Load and Process the Logo
    logo = Image.open(logo_path).convert("RGBA")

    # Resize Logo (Adjust size based on QR Code)
    logo_size = qr_img.size[0] // 5  # Pre logos are usually smaller
    logo = logo.resize((logo_size, logo_size))

    # Create White Background for Logo (To ensure readability)
    border_size = 10  # Padding around the logo
    logo_bg_size = (logo_size + 2 * border_size, logo_size + 2 * border_size)

    # Create a white background image
    logo_bg = Image.new("RGBA", logo_bg_size, (255, 255, 255, 255))

    # Paste the logo onto the white background
    logo_bg.paste(logo, (border_size, border_size), mask=logo)

    # Calculate Logo Position (Centered)
    pos = (
        (qr_img.size[0] - logo_bg_size[0]) // 2,
        (qr_img.size[1] - logo_bg_size[1]) // 2,
    )

    # Overlay the Logo on the QR Code
    qr_img.paste(logo_bg, pos, mask=logo_bg)

    # Save the Final KHQR-Style QR Code
    qr_img.save("result.png")

    # Show the Final Image
    qr_img.show()


if __name__ == "__main__":
    logo_path = input("Please input logo path: ")
    generate_khqr(logo_path=logo_path)
