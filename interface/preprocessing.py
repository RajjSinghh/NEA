import numpy
import PIL
import matplotlib.pyplot as plt
import cv2

def ImageLoader(file_name):
	image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
	retval, threshild = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)
	return image

if __name__ == '__main__':
	test_image = ImageLoader("Math_Meme-1.png")
	plt.imshow(test_image, cmap="gray")
	plt.show()
