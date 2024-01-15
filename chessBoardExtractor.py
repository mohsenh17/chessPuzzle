from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import cv2

class ChessboardExtractor:
    """
    A class for extracting chessboard information from a PDF file and performing related operations.

    Parameters:
    - path2pdf (str): The file path to the input PDF file.

    Attributes:
    - path2pdf (str): The file path to the input PDF file.
    - images (list): A list of images extracted from the PDF file.

    Example:
    >>> pdf_extractor = ChessboardExtractor('pdf/1.pdf')
    >>> pdf_extractor.pdf_to_images()
    >>> pdf_extractor.crop_header('pdf/page0.jpg')
    >>> pdf_extractor.crop_board('pdf/page0Cropped.jpg')
    >>> chessboard_coords, turn_indicator_coords = pdf_extractor.find_board('pdf/page0puzzle0.jpg')
    >>> chessboard_matrix = pdf_extractor.extract_chessboard_matrix(chessboard_coords)
    """
    def __init__(self, path2pdf):
        self.path2pdf = path2pdf
        self.images = None
        self.load_pdf_images()

    def load_pdf_images(self):
        """
        Load images from the PDF file using pdf2image library.
        """
        self.images = convert_from_path(self.path2pdf)

    def pdf_to_images(self):
        """
        Save each page of the PDF as a JPEG file.
        """
        for i, image in enumerate(self.images):
            image.save('pdf/page{}.jpg'.format(i), 'JPEG')

    @staticmethod
    def crop_header(path2img):
        """
        Crop the header of an image and save the result.

        Parameters:
        - path2img (str): The file path to the input image.

        Returns:
        None
        """
        image = cv2.imread(path2img)
        y, h = 0, 200
        cropped = image[y + h:-110]
        cv2.imwrite('pdf/page0Cropped.jpg', cropped)

    @staticmethod
    def crop_board(path2img):
        """
        Crop a chessboard from an image and save puzzle pieces.

        Parameters:
        - path2img (str): The file path to the input image.

        Returns:
        None
        """
        img = cv2.imread(path2img)
        y, h = 0, int(len(img) / 3)
        x, w = 0, int(len(img[1]) / 2)
        cropped = [
            img[y:y + h, x:x + w],
            img[y:y + h, x + w:-1],
            img[y + h:y + 2 * h, x:x + w],
            img[y + h:y + 2 * h, x + w:-1],
            img[y + 2 * h:-1, x:x + w],
            img[y + 2 * h:-1, x + w:-1]
        ]

        for i, piece in enumerate(cropped):
            cv2.imwrite('pdf/page0puzzle{}.jpg'.format(i), piece)

    @staticmethod
    def find_board(path2img):
        """
        Detect and extract the chessboard and turn indicator from an image.

        Parameters:
        - path2img (str): The file path to the input image.

        Returns:
        Tuple: A tuple containing two lists of coordinates.
            - The first list represents the bounding box of the detected chessboard.
            - The second list represents the bounding box of the detected turn indicator.
        """
        image = cv2.imread(path2img)
        blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        squares = []
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.015 * peri, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                squares.append([x, y, w, h])
        squares.sort(key=lambda x: x[3], reverse=True)
        chessboard = squares[0]
        turn_indicator = squares[-1]
        return chessboard, turn_indicator

    def extract_chessboard_matrix(self, chessboard_coords):
        """
        Extract chessboard matrix based on the provided coordinates.

        Parameters:
        - chessboard_coords (list): Coordinates of the chessboard bounding box.

        Returns:
        list: A list of chessboard matrix pieces.
        """
        x, y, w, h = chessboard_coords
        img = cv2.imread('pdf/page0puzzle0.jpg')
        chessboard_matrix = []
        for col in range(8):
            for row in range(8):
                h_start = y + int(col * h / 8)
                h_end = y + int((col + 1) * h / 8)
                w_start = x + int(row * w / 8)
                w_end = x + int((row + 1) * w / 8)
                chessboard_matrix.append(img[h_start:h_end, w_start:w_end])
        return chessboard_matrix

if __name__ == "__main__":
    pdf_extractor = ChessboardExtractor('pdf/1.pdf')
    pdf_extractor.pdf_to_images()
    pdf_extractor.crop_header('pdf/page0.jpg')
    pdf_extractor.crop_board('pdf/page0Cropped.jpg')
    chessboard_coords, turn_indicator_coords = pdf_extractor.find_board('pdf/page0puzzle0.jpg')
    chessboard_matrix = pdf_extractor.extract_chessboard_matrix(chessboard_coords)
