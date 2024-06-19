from PIL import Image

def pad_image_to_size(image_path, output_path, desired_width=800, desired_height=600):
    # Open the image
    image = Image.open(image_path)
    
    # Get current size
    current_width, current_height = image.size
    
    # Calculate padding
    left_padding = (desired_width - current_width) // 2
    right_padding = desired_width - current_width - left_padding
    top_padding = (desired_height - current_height) // 2
    bottom_padding = desired_height - current_height - top_padding
    
    # Create a new image with white background
    new_image = Image.new("RGB", (desired_width, desired_height), "white")
    
    # Paste the original image into the center of the new image
    new_image.paste(image, (left_padding, top_padding))
    
    # Save the padded image
    new_image.save(output_path)

# Example usage:
path = """
GPU-Photos/Gigabyte-GeForce-GTX-1080-Ti.jpg
""".replace('\n', '')
pad_image_to_size(path, path)
