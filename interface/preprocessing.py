import numpy
import matplotlib.pyplot as plt
import cv2

def ImageLoader(file_name): 
	"""Loading an image file using opencv"""
	image = cv2.imread(file_name, cv2.IMREAD_COLOR)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return image, gray

def FindDigits(colour, grayscale):
	"""Finding characters in an image using opencv contours"""
	#contours are sets in opencv to find a given set of pixels in an image
	#after finding contours, we can outline each set of points as a closed shape
	
	retval, threshold = cv2.threshold(grayscale, 200, 255, cv2.THRESH_BINARY_INV)
	contours, heirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(colour, contours, -1, (255, 0, 0), 0)
	return colour, grayscale, contours

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
	colour, grayscale = ImageLoader("Math_Meme-1.png")
	FindDigits(colour, grayscale)
	cv2.imshow("color", colour)
	cv2.imshow("grayscale", grayscale)
	cv2.waitKey(0)
	cv2.destroyAllWindows

