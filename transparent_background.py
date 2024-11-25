from PIL import Image


def detect_background_type(image, threshold=128):
    """
    Detects whether the background is predominantly light or dark.

    Args:
    - image (PIL.Image): The input image.
    - threshold (int): Brightness threshold (0-255). Below this is dark, above is light.

    Returns:
    - str: "light" if the background is predominantly light, "dark" if predominantly dark.
    """
    # Convert to grayscale to measure brightness
    grayscale_image = image.convert("L")
    avg_brightness = sum(grayscale_image.getdata()) / len(grayscale_image.getdata())

    return "light" if avg_brightness >= threshold else "dark"


def make_background_transparent(input_path, output_path, light_tolerance=200, dark_tolerance=50):
    """
    Automatically removes light or dark background based on its detected type.

    Args:
    - input_path (str): Path to the input image file.
    - output_path (str): Path to save the output image with transparency.
    - light_tolerance (int): Tolerance for removing light backgrounds (higher = looser).
    - dark_tolerance (int): Tolerance for removing dark backgrounds (higher = looser).
    """
    # Open the image and ensure it has an alpha channel
    image = Image.open(input_path).convert("RGBA")

    # Detect background type
    background_type = detect_background_type(image)
    print(f"Detected background type: {background_type}")

    # Get the pixel data
    data = image.getdata()
    new_data = []

    if background_type == "light":
        # Remove light background
        for item in data:
            similarity = abs(item[0] - 255) + abs(item[1] - 255) + abs(item[2] - 255)
            if similarity <= light_tolerance:
                new_data.append((255, 255, 255, 0))  # Transparent
            else:
                new_data.append(item)
    elif background_type == "dark":
        # Remove dark background
        for item in data:
            brightness = (item[0] + item[1] + item[2]) / 3
            if brightness <= dark_tolerance:
                new_data.append((0, 0, 0, 0))  # Transparent
            else:
                new_data.append(item)

    # Update the image with the new pixel data
    image.putdata(new_data)

    # Save the new image with transparency
    image.save(output_path, "PNG")
    print(f"Image saved with transparent background at {output_path}")


# Example usage
input_path = "path_to_your_image_file.png"  # Replace with your image file path
output_path = "output_image_with_transparency.png"  # Replace with the desired output path

# Tolerances for light and dark background removal
light_tolerance = 200  # Adjust for light background (higher = looser)
dark_tolerance = 50  # Adjust for dark background (higher = looser)

make_background_transparent(input_path, output_path, light_tolerance, dark_tolerance)
