import math
import json
import tensorflow
from random import *
from neuralnetwork import *

def MainMenu():
    """Menu function. The user can create a new neural network model,
       train an existing one, or quit the program 
    """
    
    #Displaying menu
    continue_flag = True
    while continue_flag:
        print("\n")
        print("Main Menu")
        print("\n")
        print("1: Create New Neural Network")
        print("2: Train Neural Network")
        print("3: Quit")
        print("\n")
        
        #Taking user input and acting accordingly
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
    #mnist is 28x28
    input_size = 784 
    flag = True
    
    while flag: #Inputting dimenstions 
        try:
            number_of_hidden = int(input("How many hidden layers do you want? "))
            hidden_size = int(input("How many hidden nodes do you want? "))
            flag = False
        except:
            print("Invalid input")

    output_size = 10

    #Creates new neural network based on parameters
    parameters = {
            "input_size": input_size,
            "number_of_hidden_layers": number_of_hidden,
            "number_of_hidden_nodes": hidden_size,
            "output_size": output_size
            }

    network = NeuralNetwork(False, parameters, {}) 
    
    #Writing out object to a file
    file_name = input("Enter a name for this model: ")

    with open(file_name+".json", "w") as file: 
       file.write(network.ToJSON()) 

def Train():
    """Full training cycle
    Needs to have stochastic gradient decent for backpropagation implemented
    Batching, training, averaging and altering
    """

    #Creating and loading the mnist dataset from tensorflow
    mnist = tensorflow.keras.datasets.mnist 
    (training_images, training_labels), (test_images, test_labels) = mnist.load_data()
  
    #Loading and rebuilding neural network model
    file_name = input("What is the name of the model you would like to train? ")
    with open(file_name + ".json", "r") as file:
        data = json.loads(file.read())
    
    network = NeuralNetwork(True, {}, data)
    
    #Converting Numpy array to list
    vector = []
    for i in training_images[1]:
        vector.append(i)
    #Runs training algorithm on single piece of data
    TrainOnSingleData(network, vector, training_labels[1])

def TrainOnSingleData(network, vector, label):
    """Training on a single point of data, helper function for Train"""
    network.ForwardPass(vector)
    network.CalculateCost(label)
    print("Total loss for sample: %r" % (network.cost))
    print("COMPLETE FOR SINGLE SAMPLE")


##############################################################################################
##############################################################################################

if __name__ == "__main__":
        MainMenu()
