from PIL import Image
import pytesseract
import numpy as np

def get_text_from_image(filename):
    img1 = np.array(Image.open(filename))
    text = pytesseract.image_to_string(img1)
    return text