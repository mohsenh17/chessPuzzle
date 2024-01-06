from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import cv2
def pdf2img(path2pdf):
    """
    Convert a PDF file to a series of images.

    Parameters:
    - path2pdf (str): The file path to the input PDF file.

    Returns:
    None

    This function uses the 'convert_from_path' function from the 'pdf2image' library
    to convert each page of the input PDF file into an image. The resulting images
    are then saved as JPEG files in the 'pdf' directory with filenames in the format
    'pageX.jpg', where X is the page number starting from 0.

    Example:
    >>> pdf2img('path/to/your/file.pdf')
    """

    images = convert_from_path('pdf/1.pdf')
    for i in range(len(images)):
        images[i].save('pdf/page'+ str(i) +'.jpg', 'JPEG')

#img = Image.open('pdf/page0.jpg')

def cropHeader(path2img): 
    """
    Crop the header of an image and save the result.

    Parameters:
    - path2img (str): The file path to the input image.

    Returns:
    None

    This function reads an image using OpenCV, crops the header portion
    (assuming a header height of 200 pixels and a bottom margin of 110 pixels),
    and saves the cropped image as 'pdf/page0Cropped.jpg'.

    Example:
    >>> cropHeader('path/to/your/image.jpg')
    """   
    image = cv2.imread(path2img)
    y=0
    x=0
    h=200
    w=0
    crop = image[y+h:-110]
    cv2.imwrite('pdf/page0Croped.jpg', crop)
    
#cropHeader('pdf/page0.jpg')

def cropBoard(path2img):
    """
    Crop a chessboard from an image and save the puzzle pieces.

    Parameters:
    - path2img (str): The file path to the input image.

    Returns:
    None

    This function reads an image using OpenCV, divides it into six puzzle pieces
    representing different sections of a chessboard, and saves each puzzle piece as
    'pdf/page0puzzle{i}.jpg', where i is the index from 0 to 5.

    Example:
    >>> cropBoard('path/to/your/image.jpg')
    """
    img = cv2.imread(path2img)
    y=0
    x=0
    h=int(len(img) / 3)
    w=int(len(img[1]) / 2)
    cropped = []
    cropped.append(img[y:y+h,x:x+w])
    cropped.append(img[y:y+h,x+w:-1])

    cropped.append(img[y+h:y+2*h, x:x+w])
    cropped.append(img[y+h:y+2*h, x+w:-1])

    cropped.append(img[y+2*h:-1, x:x+w])
    cropped.append(img[y+2*h:-1, x+w:-1])
    
    for i in range(len(cropped)):
        cv2.imwrite('pdf/page0puzzle{}.jpg'.format(i), cropped[i])

#cropBoard('pdf/page0Croped.jpg')

