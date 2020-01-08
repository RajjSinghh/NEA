import tkinter as tk
"""Need to learn how to use multi-window object orientation properly"""

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.InitWindow()
        child = None

    def InitWindow(self):
        self.master.title("Main Screen")
        self.pack()

        mark = tk.Button(self, text="Mark", command=lambda:[self.destroy, self.NewMarkWindow()]) #Create new window
        close = tk.Button(self, text="Quit", command=quit)
        details = tk.Button(self, text="Details", command=lambda:[print("hello world")])
        
        mark.pack()
        details.pack()
        close.pack()
    
    def NewMarkWindow(self):
        self.child = MarkWindow(self)

class MarkWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.InitWindow()

    def InitWindow(self):
        prompt = tk.Label(text="Enter the name of the file you want marked")
        prompt.pack()

        file_entry = tk.Entry(self.master)
        submit_button = tk.Button(self.master, text="Find File", command=lambda:[self.LoadFile(file_entry.get())])
        file_entry.pack()
        submit_button.pack()
    
    def LoadFile(self, file_path):
        if file_path[-4:].lower() not in [".png", ".jpg"]:
            self.FileTypeError()
        try:
            with open(file_path, "r") as file:
                data = file.read()
            print(data)
        except:
            print("This file is not present, please try again")#replace with better exception

    def FileTypeError(self):
        window = tk.Tk()
        window.geometry("600x100")
        label = tk.Label(master=window, text="Invalid file type, must be JPG or PNG")
        label.pack()
        confirm = tk.Button(master=window, text="Okay", command=window.destroy)
        confirm.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("400x300")
    window = MainWindow(root)
    root.mainloop()
