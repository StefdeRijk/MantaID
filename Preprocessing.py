import cv2
from cv2 import CLAHE
import numpy
from PIL import Image
def preprocess_image(original_img, img_width, img_height):
	grayscale_img = original_img.convert('L')
	if int(img_width) > 800:
		grayscale_img.resize((800, int(img_height * (img_width / 800))))
	if int(img_height) > 800:
		grayscale_img.resize((int(img_width * (img_height / 800)), 800))
	no_noise_img = cv2.medianBlur(numpy.array(grayscale_img), 5)
	clahe = cv2.createCLAHE(clipLimit=3)
	high_contrast_img = clahe.apply(no_noise_img)
	high_contrast_img = Image.fromarray(high_contrast_img)
	high_contrast_img.save("grayscale.jpg")
	cv2.xfeatures2d