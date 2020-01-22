import numpy
import PIL
import matplotlib.pyplot as plt

def ConvertImage(image):
    """Converts a raw image file into a numpy array"""
    img = PIL.Image.open(image)
    img.load()
    array = list(numpy.asarray(img, dtype="int32"))
    return array

def FindDigit(image):
    """From a given numpy array, finds characters on the page"""
    #2-Dimensional linear search for non-white pixels
    for x_pos, x in enumerate(image):
        for y_pos, y in enumerate(x):
            #in numpy, a white pixel is shown with a 0
            if y > 0:
                BoxDigit(image, x_pos, y_pos)
                y = 255
    return image

def BoxDigit(image, x_pos, y_pos):
    #these pointers refer to the boundary lines
    left_ptr = y_pos
    right_ptr = y_pos
    top_ptr = x_pos
    bottom_ptr = x_pos

    


def NormaliseDigit(digit):
    return mnist_digit

if __name__ == '__main__':
    print("hello world")
    x = FindDigit(ConvertImage("Math_Meme-1.png"))
    plt.imshow(x)
    plt.show()
