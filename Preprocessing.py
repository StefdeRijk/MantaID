import cv2
import os
import numpy
from PIL import Image
def preprocess_image(original_img):
	grayscale_img = original_img.convert('L')
	no_noise_img = cv2.medianBlur(numpy.array(grayscale_img), 5)
	clahe = cv2.createCLAHE(clipLimit=4)
	high_contrast_arr = clahe.apply(no_noise_img)
	high_contrast_img = Image.fromarray(high_contrast_arr)
	high_contrast_img.save("preprocessed_img.jpg")
	return high_contrast_img