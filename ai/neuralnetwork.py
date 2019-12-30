import random
import math
import json

def Sigmoid(x):
    """Sigmoid Activation Function"""
    return (1 + math.exp(x))**(-1)

def Softmax(v):
    """softmax takes a vector and returns that vector as a probability distribution"""
    denominator = 0
    for i in v:
        denominator += math.e**i
    output = []
    for i in v:
        output.append((math.e**i) / denominator)
    return output

class NeuralNetwork():
    """A generic neural network object -> this comment block is horribly out of date and needs re-writing
    -----------------------------------------------------------------
    VARIABLE LIST
    -----------------------------------------------------------------
    
    -----------------------------------------------------------------
    """
    class InputNeuron:
        """A simple input neuron
            
           Variables:
           value: the value held by that node
           bias: a bias to control the offset of the neuron
        """
        
        def __init__(self, value=0, bias=random.randint(-255, 255)):
            self.value = value
            self.bias = bias
        
        def SetValue(self, value):
            """Sets the value of the neuron to a passed in value and the neuron's bias"""
            self.value = value + self.bias
    
    class Neuron(InputNeuron):
        """A general neuron that takes the same parameters as the input neuron,
           but adds weights and calculates sum
           
           Variables:
           weights: a list of the weights to the previous layer of neurons
           output: a flag to say whether the given node is in the output layer
           """
        def __init__(self, number_of_prev_nodes, output):
           super().__init__()
           self.weights = []
           for i in range(number_of_prev_nodes):
               self.weights.append(random.uniform(-2, 2))
                   
           self.output = output #Boolean to see if is in output layer
        
        def WeightedSum(self, previous_layer):
            """Calculates the value of the the neuron based on the previous layer"""
            self.value = 0
            for i in range(len(previous_layer)):
                self.value += previous_layer[i].value * self.weights[i]
            self.value += self.bias

    def __init__(self, created, parameters, data): 
        """Creating the network structure
        Variables:
        inputs: a list of input neurons
        hidden: a list of lists. Inner lists contain neurons and act as layers
        outputs: a list of neurons to act as the output layer
        cost: an overall metric for how well the network classified a sample. 0 cost is best.
        """
        #Creating a new network structure based on the values presented by the user. This is stored in parameters
        
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
        
        #If the network has already been created, the values are passed into data and rebuilt here
        else:
            self.inputs = []
            self.hidden = []
            self.outputs = []
            self.cost = 0
            
            #Initialising input layer
            inputs = data["inputs"]
            for i in inputs:
                new_neuron = NeuralNetwork.InputNeuron(i["value"], i["bias"])
                self.inputs.append(new_neuron)
            
            #Initialising hidden layers
            hidden = data["hidden"]
            for i in hidden:
              new_layer = []
              for j in i:
                  new_neuron = NeuralNetwork.Neuron(10, j["output"])
                  new_neuron.weights = j["weights"]
                  new_neuron.bias = j["bias"]
                  new_layer.append(new_neuron)
              self.hidden.append(new_layer)
            
            #Initialising output layer
            outputs = data["outputs"]
            for i in outputs:
                new_neuron = NeuralNetwork.Neuron(10, True)
                new_neuron.weights = i["weights"]
                new_neuron.value = i["value"]
                new_neuron.bias = i["bias"]
                self.outputs.append(new_neuron)
        
    def FillInputVector(self, vector):
        """Setting the input layer equal to the vector passed into the function"""

        for i in range(len(self.inputs)):
            self.inputs[i].value = vector[i] 
   
    def ForwardPass(self, sample):
        """Calculating the output vector from the input vector, has to be run after inputs are defined"""
        #Initial hidden layer
        for i in self.hidden[0]:
            value = 0
            for c, j in enumerate(i.weights):
                value += j * self.inputs[c].value
            value = Sigmoid(value)
            i.value = value

        #Hidden layer
        try:
           for pointer, i in enumerate(self.hidden):
                for j in self.hidden[pointer + 1]:
                    value = 0
                    for c, k in enumerate(j.weights):
                        value += k * i[c].value
                    value = Sigmoid(value)
                    j.value = value
        except:
            pass

        #Output layer
        sum_vector = []
        for i in self.outputs:
            value = 0
            for c, j in enumerate(i.weights):
                value += j * self.hidden[-1][c].value
            sum_vector.append(value)
        
        output_vector = Softmax(sum_vector)
        for c, i in enumerate(self.outputs):
            i.value = output_vector[c]

        for i in self.outputs:
            print(i.value)

    def CalculateCost(self, label):
        """Cost is a measure of how well the neural network has performed on the given task"""
        cost = 0

        print(label)
        errors = [] 
        #Cost here is the sum of the squares of the differences between outputs and truth
        for i in range(len(self.outputs)):
            if i == label:
                cost += (1 - self.outputs[i].value)**2
                errors.append((self.outputs[i].value - 1)**2)
            else:
                cost += (self.outputs[i].value)**2
                errors.append((self.outputs[i].value)**2)
        self.cost = cost / len(self.outputs)
        print("--------------------")
        print("Errors")
        for i in errors:
            print(i)
        return errors
    
    def ToJSON(self): #Simple JSON serializer
        """Returns object rather than an object, this means that I have no way of calling class
           methods in a  load function """
        return json.dumps(self, default=lambda o:o.__dict__, indent=4) 
