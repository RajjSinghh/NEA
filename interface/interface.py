import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from preprocessing import *
import tensorflow as tf
import numpy as np

class MenuWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.geometry = ("600x400")
		welcome = tk.Label(self, text="Welcome to the AI Marking System")
		welcome.pack()
		mark = tk.Button(self, text="Mark Work", command=MarkWindow)
		mark.pack()
		
		self.quit = tk.Button(self, text="Quit", command=self.destroy)
		self.quit.pack()

class MarkWindow(tk.Tk):
	def __init__(self):	
		super().__init__()
		self.entry = EntryWindow()
		self.file_path = self.entry.text
		self.load = tk.Button(self, text="load image", command=self.GetEntryText)
		self.load.pack()
		self.mark_button = tk.Button(text="Mark", command=self.Mark)
		self.mark_button.pack()
		self.text = ""
		self.image = None
		self.threshold = None
		self.model = tf.keras.models.load_model("better.model")
		self.CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "*", "/", "-"]	
		##Add a display using matplotlib or cv2?
		##Poll entry window for text and if text != none, destroy entry
	
	def GetEntryText(self):
		self.text = self.entry.text
		self.Display()
	
	def Display(self):
		self.image = cv2.imread(self.text, cv2.IMREAD_COLOR)
		self.image_grayscale = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		self.digits, self.contours = Process(self.image, self.image_grayscale)
		plt.imshow(self.image)
		plt.show()

	def Mark(self):
		for c, line in enumerate(self.digits):
			prediction = self.model.predict(np.array(line))
			for c, i in enumerate(line):
				print(np.argmax(prediction[c]))
				plt.imshow(i)
				plt.show()
				question = ""
			for char in prediction:
				question += self.CHARS[np.argmax(char)]
			print(question)

class EntryWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		prompt = tk.Label(self, text="Enter the file name you are looking for")
		self.entry = tk.Entry(self)
		prompt.pack()
		self.entry.pack()
		self.submit = tk.Button(self, text="Submit", command=self.ValidateEntry)
		self.submit.pack()
		self.text = ""

	def ValidateEntry(self):
		text = "bin/" + self.entry.get()
		flag = False
		
		if text[-4:] not in [".png", ".jpg", ".gif"]:
			self.error = ErrorWindow("Not a supported file type")
		else:
			try:
				with open(text, "r") as file:
					flag = True
			except FileNotFoundError:
				self.error = ErrorWindow("This file does not exist")
		if flag:
			self.text = text
		
class ErrorWindow(tk.Tk):
	def __init__(self, message):
		super().__init__()
		self.label = tk.Label(self, text=message)
		self.label.pack()
		self.close = tk.Button(self, text="Close", command=self.destroy)
		self.close.pack()

if __name__ == '__main__':
	main_menu = MenuWindow()
	tk.mainloop()
