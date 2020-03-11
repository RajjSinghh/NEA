import numpy
import matplotlib.pyplot as plt
import cv2

def ImageLoader(file_name): 
	"""Loading an image file using opencv"""
	image = cv2.imread(file_name, cv2.IMREAD_COLOR)
	#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#return image, gray
	return image

def FindDigits(colour, grayscale):
	"""Finding characters in an image using opencv contours"""
	#contours are sets in opencv to find a given set of pixels in an image
	#after finding contours, we can outline each set of points as a closed shape
	
	retval, threshold = cv2.threshold(grayscale, 200, 255, cv2.THRESH_BINARY_INV)
	contours, heirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(colour, contours, -1, (255, 0, 0), 0)
	return colour, grayscale, contours

def NormaliseDigit(image, contour):
	#The box the image is in will be top left to bottom right, so these corners are the 
	#smallest x value and y value respectively
	small_x = contour[0][0][0]
	large_y = contour[0][0][1]
	top_left = contour[0][0]
	bottom_right = contour[0][0]
	for i in contour:
		if i[0][0] < small_x:
			small_x = i[0][0]
			top_left = i
		if i[0][1] < large_y:
			large_y = i[0][1]
			bottom_right = i

	##TODO Finish troubleshooting this image slicing system and begin work on a 
	##translation and scaling system
#	print(top_left)
#	print(bottom_right)
#	print(image[top_left[0] : bottom_right[0], top_left[1] : bottom_right[1] ])
#	cv2.imshow("mat", image[[top_left[0]:bottom_right[0]] [top_left[1]:bottom_right[1]]])
#	cv2.waitKeyPressed(0)
#	cv2.destroyAllWindows()
		

if __name__ == '__main__':
	colour, grayscale = ImageLoader("Math_Meme-2.png")
	colour, grayscale, contours = FindDigits(colour, grayscale)
	print(contours[0].shape)
	NormaliseDigit(colour, contours[0])
	cv2.imshow("color", colour)
	cv2.imshow("grayscale", grayscale)
	cv2.waitKey(0)
	cv2.destroyAllWindows

