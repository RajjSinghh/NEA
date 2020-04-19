import numpy as np
import matplotlib.pyplot as plt
import cv2

def FindDigits(image, grayscale):
	"""Finding characters in an image using opencv contours"""
	#contours are sets in opencv to find a given set of pixels in an image
	#after finding contours, we can outline each set of points as a closed shape
	retval, threshold = cv2.threshold(grayscale, 200, 255, cv2.THRESH_BINARY_INV)
	contours, heirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#	cv2.drawContours(image, contours, -1, (255, 0, 0), 0)
	return image, grayscale, contours

def QuickSort(lst, low, high, key=lambda x:x):
	if low < high:
		p = Partition(lst, low, high, key)
		QuickSort(lst, low, p - 1)
		QuickSort(lst, p + 1, high)

def Partition(lst, low, high, key):
	pivot = key(lst[high])
	i = low
	for j in range(low, high + 1):
		if key(lst[j]) < pivot:
			lst[i], lst[j] = lst[j], lst[i]
			i += 1
	lst[i], lst[high] = lst[high], lst[i]
	return i

def EraseInnerHelper(line, c):
	index = 0
	while index < len(line) -1:	
		x, y, w, h = cv2.boundingRect(line[index])
		initial = [x, y, w, h]
		x, y, w, h = cv2.boundingRect(line[index + 1])
		next_val = [x, y, w, h]

		if next_val[0] > initial[0] and next_val[0] < initial[0]  + initial[2]:
			print("got one")
			line.pop(index + 1)
			index -= 1
		index += 1
	c.append(line)

	
def EraseInner(contours, image, grayscale):
	c = []
	for line in contours:
		EraseInnerHelper(line, c)
	for line in contours:
		EraseInnerHelper(line, c)
	return c

def DetectLines(contours):
	"""Function to change contours to sets of sorted lines"""	
	c = []
	cnt_left = contours
	while cnt_left:
		new_line = []
		for cnt in reversed(contours):
			temp = cnt.reshape((len(cnt), 2))
			if new_line == []:
				new_line.append(cnt)
			else:
				prev = new_line[-1].reshape((len(new_line[-1]), 2))
				if temp[0][1] - prev[0][1] > 15:
					c.append(new_line)
					break
				else:
					new_line.append(cnt)
			cnt_left.pop()
	c.append(new_line)
	
	sorted_x = []

	for line in c:
		new_line = sorted(line, key=lambda x:x.reshape((len(x), 2))[0][0])  ##replace with Quicksort
		sorted_x.append(new_line)

	return sorted_x

def Process(image, grayscale):
	image, grayscale, contours = FindDigits(image, grayscale)
	contours = DetectLines(contours)
	contours = EraseInner(contours, image, grayscale)
	digits = []
	for line in contours:
		digits.append([])
		for digit in line:
			x, y, w, h = cv2.boundingRect(digit) 
			sample = grayscale[ y-1: y+h+1, x - 1: x +w + 1,]
			sample = cv2.resize(sample, (28, 28))
			sample = cv2.bitwise_not(sample)
			digits[-1].append(sample)
	return digits

	

if __name__ == '__main__':
	image = cv2.imread('bin/printed.jpg')
	grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#	image, grayscale, contours = FindDigits(image, grayscale)
##	print(grayscale)
##	plt.imshow(grayscale)
##	plt.show()
##	for cnt in contours:
##		x, y, w, h = cv2.boundingRect(cnt)
##		#cv2.rectangle(grayscale, (x, y), (x+w, y+h), (0, 255, 0), 2)
##		sample = grayscale[y-1:y+h+1,x-1:x+w+1]
##		sample = cv2.bitwise_not(sample)
##		print(sample.shape)
##		sample = cv2.resize(sample, (28, 28))	
##		plt.imshow(sample)
##		plt.show()
##	
##	contours = reversed(contours)
##	x = []
##	img = image
##	for cnt in contours:
##		x.append(cnt)
##		cv2.drawContours(img, x, -1, (255, 0, 0), 0)
##		plt.imshow(img)
##		plt.show()
##
#
##	print(contours)
#	img = image
#	cont = DetectLines(contours)
#	
#
#	print(len(cont))
##	for ln in cont:
##		print(ln)
##		for c in ln:
##			print(c.reshape((len(c), 2)))
##			img = cv2.drawContours(img, c, -1, (0, 255, 0), 0)
##			plt.imshow(img)
##			plt.show()
#
#	contours = EraseInner(cont, img, grayscale)
#	
#	for line in contours:
#		cv2.drawContours(image, line, -1, (255, 0, 0), 0)
#	plt.imshow(image)
#	plt.show()
### have 22, must have around 6000 for train and 1000 for test	
##	count = 0
##	for line in contours:
##		symbol = 0
##		for a in line:
##			x, y, w, h = cv2.boundingRect(a)
##			sample = grayscale[y - 1:y+h +1, x - 1:x + w + 1]
##			sample = cv2.resize(sample, (28, 28))
##			sample = cv2.bitwise_not(sample)
##			cv2.imwrite(f"data/{count}.jpg", sample)
##			count += 1
#			
#

	digits = Process(image, grayscale)
	for line in digits:
		for digit in line:
			plt.imshow(digit)
			plt.show()
	cv2.imshow("grayscale", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
