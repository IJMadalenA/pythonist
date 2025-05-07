import os
import urllib.request
from urllib.error import URLError

import segno


def generate_qr(
    content: str,
    filename: str = "qr_code",
    scale: int = 5,
    border: int = 2,
    color: str = "black",
    background: str = None,
    output_format: str = "svg",
) -> str:
    """
    Generates a QR code and saves it in the specified format.
    Enhanced with error handling.

    :param content: Text or URL to encode in the QR code.
    :param filename: Name of the output file (without extension).
    :param scale: Scaling factor for the QR code (default: 5).
    :param border: Border size (default: 2).
    :param color: QR code color (default: black).
    :param background: Background color (optional).
    :param output_format: Output file format (svg, png, pdf, etc.).
    :return: Path to the generated file or error message.
    """
    try:
        if output_format not in ["svg", "png", "pdf", "eps", "jpeg"]:
            raise ValueError(
                f"Invalid output format '{output_format}'. Choose from: svg, png, pdf, eps, jpeg."
            )

        qr = segno.make(content)

        options = {"scale": scale, "border": border, "dark": color}
        if background:
            options["light"] = background

        file_path = f"{filename}.{output_format}"
        qr.save(file_path, **options)

        return file_path
    except Exception as e:
        return f"Error generating QR code: {str(e)}"


def generate_artistic_qr(
    content: str,
    background_source: str,
    filename: str = "artistic_qr",
    scale: int = 5,
) -> str:
    """
    Generates an artistic QR code with an image or GIF background from a URL or local file.

    :param content: Text or URL to encode in the QR code.
    :param background_source: URL or local file path of the background image/GIF.
    :param filename: Name of the output file (without extension).
    :param scale: Scaling factor for the QR code.
    :return: Path to the generated file or an error message.
    """
    try:
        # Determine if background_source is a URL or local file
        if background_source.startswith(("http://", "https://")):
            background = urllib.request.urlopen(background_source)
            file_ext = os.path.splitext(background_source)[-1].lower()
        else:
            if not os.path.exists(background_source):
                return "Error: Local file does not exist."
            background = background_source
            file_ext = os.path.splitext(background_source)[-1].lower()

        # Choose the appropriate output format based on background type
        output_format = "gif" if file_ext in [".gif"] else "png"
        target_file = f"{filename}.{output_format}"

        qr = segno.make(content)
        qr.to_artistic(
            background=background,
            target=target_file,
            scale=scale,
        )

        return target_file

    except URLError:
        return "Error: Unable to download the background image. Check the URL."
    except Exception as e:
        return f"Error generating artistic QR code: {str(e)}"


# Example usage:
generate_artistic_qr(
    "https://www.youtube.com/watch?v=hTWKbfoikeg",
    "https://media.giphy.com/media/LpwBqCorPvZC0/giphy.gif",
)


# Example usage
generate_qr(content="https://github.com/IJMadalena", output_format="png")
