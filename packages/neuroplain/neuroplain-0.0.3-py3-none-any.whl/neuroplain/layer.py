import time
import numpy as np

class Layer:

    def __init__(self, input_size, output_size, activation_function):
        np.random.seed(seed=int(time.time())) 
        self.weights = np.random.randn(output_size, input_size) * np.sqrt(2. / input_size)
        self.biases = np.zeros((output_size, 1))
        self.activation_function = activation_function
        self.output = None
        self.input = None
        self.weight_gradient = None
        self.bias_gradient = None

    def forward(self, input_data):
        self.input = input_data
        z = np.dot(self.weights, input_data) + self.biases
        self.output = self.activation_function.function(z)
        return self.output

    def backward(self, output_gradient, learning_rate):
        activation_derivative = self.activation_function.derivative(self.output)
        delta = output_gradient * activation_derivative
        self.weight_gradient = np.dot(delta, self.input.T)
        self.bias_gradient = np.sum(delta, axis=1, keepdims=True)
        self.weights -= learning_rate * self.weight_gradient
        self.biases -= learning_rate * self.bias_gradient
        return np.dot(self.weights.T, delta)