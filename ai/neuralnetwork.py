import random
import time
import math
import json
"""Currently the sums are getting too big"""

def Sigmoid(x):
    """Sigmoid Activation Function"""
    try:
        return (1 + math.exp(x))**(-1)
    except OverflowError:
        if x > 0:
            return (1 + math.exp(float("inf")))**(-1)
        else:
            return (1 + math.exp(-float("inf")))**(-1)



class NeuralNetwork():
    """A generic neural network object -> this comment block is horribly out of date and needs re-writing
    -----------------------------------------------------------------
    VARIABLE LIST
    -----------------------------------------------------------------
    input_size: the number of nodes in the input layer
    number_of_hidden: the number of hidden layers
    hidden_size: the number of nodes in the hidden layer
    output_size: number of nodes in the output layer
    activation_function: a string containing the name of the
                         activation function I use, Relu and 
                         Sigmoid are currently defined, Relu 
                         used by default
    -----------------------------------------------------------------
    """
    class InputNeuron:
        """A simple input neuron"""
        
        def __init__(self, value=0, bias=random.randint(-255, 255)):
            self.value = value
            self.bias = bias
        
        def SetValue(self, value):
            self.value = value + self.bias
    
    class Neuron(InputNeuron):
        """A general neuron that takes the same parameters as the input neuron,
           but adds weights and calculates sum"""
        def __init__(self, number_of_prev_nodes, output):
           super().__init__()
           self.weights = []
           for i in range(number_of_prev_nodes):
               self.weights.append(random.uniform(-2, 2))
                   
           self.output = output #Boolean to see if is in output layer
        
        def WeightedSum(self, previous_layer):
            #Calculates the weighted sum of a neuron by multiplying weights by the value in the neuron before
            value = 0
            for count, i in enumerate(self.weights):
                value += i * previous_layer[count].value
            value += self.bias
            self.value = Sigmoid(value)
            print(self.value)

    def __init__(self, created, parameters, data): 
        """Creating the network structure"""
        if not created:
            self.inputs = [NeuralNetwork.InputNeuron() for i in range(parameters["input_size"])] 
            
            self.hidden = [[] for i in range(parameters["number_of_hidden_layers"])]
            for i in range(parameters["number_of_hidden_layers"]):
                if i == 0:
                    for layer in range(parameters["input_size"]):
                        node = NeuralNetwork.Neuron(parameters["input_size"], False)
                        self.hidden[i].append(node)
                else:
                    for layer in range(parameters["number_of_hidden_nodes"]):
                        node = NeuralNetwork.Neuron(parameters["number_of_hidden_nodes"], False)
                        self.hidden[i].append(node)

            self.outputs = [NeuralNetwork.Neuron(parameters["number_of_hidden_nodes"], True) for i in range(parameters["output_size"])]
            self.loss = 0
        
        else:
            self.inputs = []
            self.hidden = []
            self.outputs = []
            self.cost = 0

            inputs = data["inputs"]
            for i in inputs:
                new_neuron = NeuralNetwork.InputNeuron(i["value"], i["bias"])
                self.inputs.append(new_neuron)
            
            hidden = data["hidden"]
            for i in hidden:
              new_layer = []
              for j in i:
                  new_neuron = NeuralNetwork.Neuron(10, j["output"])
                  new_neuron.weights = j["weights"]
                  new_neuron.bias = j["bias"]
                  new_layer.append(new_neuron)
              self.hidden.append(new_layer)

            outputs = data["outputs"]
            for i in outputs:
                new_neuron = NeuralNetwork.Neuron(10, True)
                new_neuron.weights = i["weights"]
                new_neuron.value = i["value"]
                new_neuron.bias = i["bias"]
                self.outputs.append(new_neuron)

            
            self.loss = data["loss"]
        
    def FillInputVector(self, vector):
        """Setting the input layer equal to the vector passed into the function"""
        for c, i in enumerate(vector):
            self.inputs[c].SetValue(i)
            print(self.inputs[c].value)
    
    def ForwardPass(self, sample):
        """Calculating the output vector from the input vector, has to be run after inputs are defined"""

        #Set input vector
        self.FillInputVector(sample)
        time.sleep(15)

        #Calculates sum of first hidden layer
        for i in self.hidden[0]:
            i.WeightedSum(self.inputs)
            print(i.value)

        
        
        #try:
        #   for pointer, i in enumerate(self.hidden):
        #        for j in self.hidden[pointer + 1]:
        #            value = 0
        #            for c, k in enumerate(j.weights):
        #                value += k * i[c].value
        #            value = Sigmoid(value)
        #            j.value = value
        #except:
        #    pass

        #for i in self.outputs:
        #    value = 0
        #    for c, j in enumerate(i.weights):
        #        value += j * self.hidden[-1][c].value
        #    value = Sigmoid(value)
        #    i.value = value

        for pointer, i in enumerate(self.hidden[1:]):
            for j in i:
                j.WeightedSum(self.hidden[pointer])

        for i in self.outputs:
            i.WeightedSum(self.hidden[-1])
            print(i.value)
    
    ##################################################################################################################
    
    def CalculateCost(self, label):
        """Loss is a measure of how well the neural network has performed on the given task"""
        cost = 0
        for i in range(len(self.outputs)):
            if i == label:
                cost += (self.outputs[i].value - 1)**2
            else:
                cost += (self.outputs[i].value)**2
        self.cost = cost
        return cost
    
    def ToJSON(self): #Simple JSON serializer
        """Returns object rather than an object, this means that I have no way of calling class
           methods in a  load function """
        return json.dumps(self, default=lambda o:o.__dict__, indent=4) 
