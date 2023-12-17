from PIL import Image, ImageOps, ImageFilter

def add_frame_and_blur_background(image_path, output_path):
    # Load the image
    original_image = Image.open(image_path)
    
    # Calculate the aspect ratio
    aspect_ratio = original_image.width / original_image.height
    
    # Determine the new size maintaining the aspect ratio within a 16:9 frame
    if aspect_ratio > 16 / 9:  # Landscape
        new_width = 1920
        new_height = int(new_width / aspect_ratio)
    else:  # Portrait or square
        raise "not implemented"
        new_height = 1080
        new_width = int(new_height * aspect_ratio)
    
    # Resize the image to the new size
    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    
    # Create a new image with a white background and 16:9 aspect ratio
    new_image = Image.new("RGB", (1920, 1080), "white")
    
    # Calculate positioning to center the image
    x = (1920 - new_width) // 2
    y = (1080 - new_height) // 2
    
    # Paste the resized image onto the center of the background
    new_image.paste(resized_image, (x, y))
    
    # Create a blurred background image from the original
    blur_radius = 15  # The radius can be adjusted for the desired blur effect
    blurred_background = original_image.resize((1920, 1080), Image.NEAREST).filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Combine the blurred background with the new image, using the new image as a mask
    combined_image = Image.composite(new_image, blurred_background, new_image.convert("L"))
    
    # Save the result
    combined_image.save(output_path)

# The path to the original image and the output path
original_image_path = r'D:\1_pywk\_DSC2375.jpg'
output_image_path = r'D:\1_pywk\new__DSC2375.jpg'

# Call the function to add the frame and blur the background
add_frame_and_blur_background(original_image_path, output_image_path)

output_image_path
