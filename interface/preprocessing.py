import numpy
import PIL
import matplotlib.pyplot as plt
def ConvertImage(image):
    img = PIL.Image.open(image)
    img.load()
    array = numpy.asarray(img, dtype="int32")
    return array

def FindDigit(image):
    pass

def NormaliseDigit(digit):
    return mnist_digit

if __name__ == '__main__':
    print("hello world")
    x = ConvertImage("Math_Meme-1.png")
    plt.imshow(x)
    plt.show()
