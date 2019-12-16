import random
import json
"""Refactor this"""

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
            self.value = 0
            for i in range(len(previous_layer)):
                self.value += previous_layer[i].value * self.weights[i]
            self.value += self.bias

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
            self.loss = 0

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
        
    def Relu(x):
        """Relu activation function"""
        return max(0, x)
    
    def Sigmoid(x):
        """Sigmoid Activation Function"""
        return (1 + math.exp(x))**(-1)

    def FillInputVector(self, vector):
        """Setting the input layer equal to the vector passed into the function"""

        for i in range(len(self.inputs)):
            self.inputs[i].value = vector[i] 
   ###################################################################################################################


    def SumOfLayer(self, layer, sample, pointer):
        """in the hidden cases, i is a list rather than a neuron and therefore has no weighted sum."""
        for i in range(len(layer)):
            if layer[i] in self.outputs:#Output layer
                layer[i].WeightedSum(self.SumOfLayer(self.hidden, sample, -1)) 
            elif layer[i] in self.inputs:#input layer
                layer[i].SetValue(sample[i])
            else: #if i in self.hidden
                if pointer == -len(self.hidden):
                     self.SumOfLayer(self.inputs, sample, None)
                else:
                     self.SumOfLayer(self.hidden[pointer - 1], sample, pointer - 1)
                
                for j in self.hidden[pointer]:
                    if pointer != -len(self.hidden):
                        j.WeightedSum(self.hidden[pointer - 1]) 
                    else:
                        j.WeightedSum(self.inputs)


    def ForwardPass(self, sample):
        """Calculating the output vector from the input vector, has to be run after inputs are defined"""
        self.SumOfLayer(self.outputs, sample, None)
        for i in self.outputs:
            print(i.value)


############################################################################################################
    def CalculateLoss(self, label):
        """Loss is a measure of how well the neural network has performed on the given task"""

        loss = 0
        for i in range(len(self.outputs)):
            if i == label:
                loss += (self.outputs[i].value - 1)**2
            else:
                loss += (self.outputs[i])**2
        self.loss = loss
        return loss
    
    def ToJSON(self): #Simple JSON serializer
        """Returns object rather than an object, this means that I have no way of calling class
           methods in a  load function """
        return json.dumps(self, default=lambda o:o.__dict__, indent=4) 
