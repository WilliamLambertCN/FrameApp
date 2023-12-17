
from matplotlib import pyplot as plt
import cv2
import numpy as np

parent="D:/1_pywk/FrameApp/"

def blur_bg(original_image,wh_ratio,screen,blur_radius=50):
    screen_width=screen[1]
    screen_height=screen[0]
    if abs(wh_ratio-16/9)<1e-5:
        blurred_background = cv2.resize(original_image, (int(screen_height*wh_ratio), screen_height), interpolation=cv2.INTER_AREA)
    else:
        blurred_background = cv2.resize(original_image, (screen_width, int(screen_width/wh_ratio)), interpolation=cv2.INTER_AREA)
        
    # Create a blurred background image from the original
    blurred_background = cv2.GaussianBlur(blurred_background, (0, 0), blur_radius)
    
    bg_x=(blurred_background.shape[1]-screen_width)//2
    bg_y=(blurred_background.shape[0]-screen_height)//2
    
    blurred_background=blurred_background[bg_y:bg_y+screen_height,bg_x:bg_x+screen_width]
    
    return blurred_background

def horizon_image(original_image,wh_ratio, logo_path,screen):
    screen_width=screen[1]
    screen_height=screen[0]
    resized_height = int(screen_height * 0.71)
    resized_width = int(resized_height * wh_ratio)
    # Resize the image to the new size
    resized_image = cv2.resize(original_image, (resized_width, resized_height), interpolation=cv2.INTER_LANCZOS4)
    
    # Create a new image with a white background and 16:9 aspect ratio
    frame = np.full((int(screen_height), int(screen_height * 1.17), 3), 255, dtype=np.uint8)
    
    # Calculate positioning to center the image
    x = (frame.shape[1] - resized_width) // 2
    y = frame.shape[0] // 17
    
    # Paste the resized image onto the center of the background
    frame[y:y+resized_height, x:x+resized_width] = resized_image
    
    # Load and resize the logo
    logo = cv2.imread(logo_path, cv2.IMREAD_COLOR)
    rto_logo = logo.shape[1] / logo.shape[0]
    logo_height = screen_height // 10
    logo_width = int(logo_height * rto_logo)
    logo = cv2.resize(logo, (logo_width, logo_height), interpolation=cv2.INTER_AREA)
    
    logo[cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)>128]=(255,255,255)
    logo[cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)<=128]=(0,0,0)
    
    # Paste the logo onto the image
    lx = (frame.shape[1] - logo_width) // 2
    ly = int(8.5 * frame.shape[0] // 10)
    
    frame[ly:ly+logo_height, lx:lx+logo_width]=logo

    return frame

def vertical_image(original_image,wh_ratio, logo_path,screen):
    screen_width=screen[1]
    screen_height=screen[0]
    # return frame, blurred_background
    resized_height = int(screen_height * 0.85)
    resized_width = int(resized_height * wh_ratio)
    # Resize the image to the new size
    resized_image = cv2.resize(original_image, (resized_width, resized_height), interpolation=cv2.INTER_LANCZOS4)
    
    # Create a new image with a white background and 16:9 aspect ratio, height, width, channel
    frame = np.full((int(screen_height), int(screen_height * 0.62), 3), 255, dtype=np.uint8)
    
    # Calculate positioning to center the image
    x = (frame.shape[1] - resized_width) // 2
    y = int(0.043*resized_height)
    
    # Paste the resized image onto the center of the background
    frame[y:y+resized_height, x:x+resized_width] = resized_image
    
    # Load and resize the logo
    logo = cv2.imread(logo_path, cv2.IMREAD_COLOR)
    rto_logo = logo.shape[1] / logo.shape[0]
    logo_height = int(screen_height*0.055)
    logo_width = int(logo_height * rto_logo)
    logo = cv2.resize(logo, (logo_width, logo_height), interpolation=cv2.INTER_AREA)
    
    logo[cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)>128]=(255,255,255)
    logo[cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)<=128]=(0,0,0)
    
    # Paste the logo onto the image
    lx = (frame.shape[1] - logo_width) // 2
    ly = int(17.01*logo_height)
    
    frame[ly:ly+logo_height, lx:lx+logo_width]=logo
    
    return frame


def add_frame_and_blur_background_opencv(image_path, output_path,logo_path=parent+"logos/Nikon Logo.png",screen=(2160,3840)):
    # Load the image
    original_image = cv2.imread(image_path)
    
    # Calculate the aspect ratio
    wh_ratio = original_image.shape[1] / original_image.shape[0] 
    
    # Determine the new size maintaining the aspect ratio within a 16:9 frame
    if wh_ratio > 1:  # Landscape
        frame=horizon_image(original_image,wh_ratio, logo_path,screen)
    else:  # Portrait or square
        frame=vertical_image(original_image,wh_ratio, logo_path,screen)
        
    blurred_background = blur_bg(original_image,wh_ratio,screen)
    
    # Calculate the position to paste the original image on the blurred background
    left = (blurred_background.shape[1] - frame.shape[1]) // 2
    top = (blurred_background.shape[0] - frame.shape[0]) // 2
    
    # Paste the original image on the blurred background
    blurred_background[top:top+frame.shape[0], left:left+frame.shape[1]] = frame
    
    # Save the result
    cv2.imwrite(output_path, blurred_background)
    
    plt.figure(2)
    plt.imshow(blurred_background[...,::-1])
    plt.show()


# The path to the original image and the output path
# original_image_path = r'D:\1_pywk\_DSC2375-1.jpg'
# output_image_path = r'D:\1_pywk\new__DSC2375-1.jpg'

original_image_path = r'D:\1_pywk\_DSC2375.jpg'
output_image_path = r'D:\1_pywk\new__DSC2375.jpg'

# Call the function to add the frame and blur the background
add_frame_and_blur_background_opencv(original_image_path, output_image_path)
