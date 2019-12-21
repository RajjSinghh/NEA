import math
import json
import tensorflow
from random import *
from neuralnetwork import *

def MainMenu():

    continue_flag = True
    while continue_flag:
        print("\n")
        print("Main Menu")
        print("\n")
        print("1: Create New Neural Network")
        print("2: Train Neural Network")
        print("3: Quit")
        print("\n")
        choice = input("What would you like to do? ")

        if choice == "1":
            CreateNeuralNetwork()

        elif choice == "2":
            Train()

        elif choice == "3":
            continue_flag = False

        else:
            print("Input not recognised, try again. ")

def CreateNeuralNetwork():
    """Creating a new instance of a neural network and allowing the user to write this out to a file"""
    print("Creating neural network for MNIST dataset")
    input_size = 784 #mnist is 28x28
    flag = True
    
    while flag: #Inputting dimenstions 
        try:
            number_of_hidden = int(input("How many hidden layers do you want? "))
            hidden_size = int(input("How many hidden nodes do you want? "))
            flag = False
        except:
            print("Invalid input")

    output_size = 10

    parameters = {
            "input_size": input_size,
            "number_of_hidden_layers": number_of_hidden,
            "number_of_hidden_nodes": hidden_size,
            "output_size": output_size
            }

    network = NeuralNetwork(False, parameters, {})
    
    file_name = input("Enter a name for this model: ")

    with open(file_name+".json", "w") as file: #Writing out to a file
       file.write(network.ToJSON()) 

def Train():
    """Full training cycle"""

    mnist = tensorflow.keras.datasets.mnist #Creating and loading the mnist dataset from tensorflow
    (training_images, training_labels), (test_images, test_labels) = mnist.load_data()

    #ADD JSON PARSER
  
    file_name = input("What is the name of the model you would like to train? ")
    with open(file_name + ".json", "r") as file:
        data = json.loads(file.read())
    
    network = NeuralNetwork(True, {}, data)
    #print(network.inputs)
#    sys.setrecursionlimit(30)
 #   for pointer in range(len(training_images)): #Convering mnist to a list and training on it
  #      vector = []
   #     for i in training_images[pointer]:
    #        for j in i:
     #           vector.append(j)

    vector = []
    for i in training_images[1]:
        for j in i:
            vector.append(j)

    TrainOnSingleData(network, vector, training_labels[1])

def TrainOnSingleData(network, vector, label):
    network.ForwardPass(vector)
    network.CalculateCost(label)
    print("Total loss for sample: %r" % (network.cost))
    print("COMPLETE RUN")


##############################################################################################
##############################################################################################

if __name__ == "__main__":
        MainMenu()
