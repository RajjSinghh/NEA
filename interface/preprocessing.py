import numpy
import matplotlib.pyplot as plt
import cv2

def ImageLoader(file_name):
	"""Loading an image file using opencv"""
	image = cv2.imread(file_name)
	imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	retval, threshold = cv2.threshold(imgray, 254, 255, 0)
	return imgray, threshold

def FindDigits(image, threshold):
	"""Finding characters in an image using opencv contours"""
	#contours are sets in opencv to find a given set of pixels in an image
	#after finding contours, we can outline each set of points as a closed shape
	contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
	print(contours[0])
	print(contours[0][0])
	print(contours[0][0][0])
	return image, contours

def BoxImage(image, contours):
	"""Cut out the digit from an image based on its contours"""
	#tracking x and y values using sets
	x = set({})
	y = set({})
	for i in contours:
		x.add(i[0][0])
		y.add(i[0][1])
	#print(x)
	#print(y)
	for i in range(max(x)):
		if i not in x:
			print(i)
	for i in range(max(y)):
		if i not in y:
			print(i)

if __name__ == '__main__':
	test_image, threshold = ImageLoader("Math_Meme-1.png")
	print(type(test_image))
	test_image, contours = FindDigits(test_image, threshold)
	BoxImage(test_image, contours[0])
	cv2.imshow("test", test_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
