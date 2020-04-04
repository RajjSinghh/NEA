import numpy as np
import matplotlib.pyplot as plt
import cv2

def FindDigits(image, grayscale):
	"""Finding characters in an image using opencv contours"""
	#contours are sets in opencv to find a given set of pixels in an image
	#after finding contours, we can outline each set of points as a closed shape
	retval, threshold = cv2.threshold(grayscale, 200, 255, cv2.THRESH_BINARY_INV)
	contours, heirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(image, contours, -1, (255, 0, 0), 0)
	return image, grayscale, contours

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
	

if __name__ == '__main__':
	image = cv2.imread('bin/printed.jpg')
	grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image, grayscale, contours = FindDigits(image, grayscale)
	print(grayscale)
	plt.imshow(grayscale)
	plt.show()
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		#cv2.rectangle(grayscale, (x, y), (x+w, y+h), (0, 255, 0), 2)
		sample = grayscale[y:y+h,x:x+w]
		sample = cv2.bitwise_not(sample)
		print(sample.shape)
		try:
			sample.reshape(28, 28) ##Replace with appropriate slicing of image	
			plt.imshow(sample)
			plt.show()
		except:
			pass	


	#print(contours[0].shape)
	#NormaliseDigit(image, contours[0])
	cv2.imshow("color", image)
	cv2.imshow("grayscale", grayscale)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

