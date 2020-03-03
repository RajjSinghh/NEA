import tkinter as tk

class MenuWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.geometry = ("600x400")
		welcome = tk.Label(self, text="Welcome to the AI Marking System")
		welcome.pack()
		mark = tk.Button(self, text="Mark Work", command=lambda:MarkWindow())
		mark.pack()
		
		self.quit = tk.Button(self, text="Quit", command=self.destroy)
		self.quit.pack()

class MarkWindow(tk.Tk):
	def __init__(self):	
		super().__init__()
		self.entry = EntryWindow()
		self.file_path = self.entry.text
		
		##Add a display using matplotlib or cv2?
		##Poll entry window for text and if text != none, destroy entry

class EntryWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		prompt = tk.Label(self, text="Enter the file name you are looking for")
		self.entry = tk.Entry(self)
		prompt.pack()
		self.entry.pack()
		self.submit = tk.Button(self, text="Submit", command=self.ValidateEntry)
		self.submit.pack()
	
	def ValidateEntry(self):
		text = self.entry.get()
		flag = False
		print(text[-4])
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
