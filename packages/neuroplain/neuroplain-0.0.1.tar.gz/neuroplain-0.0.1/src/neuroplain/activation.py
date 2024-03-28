import numpy as np

class ActivationFunction:

    class Sigmoid():
        
        @staticmethod
        def function(x):
            return 1 / (1 + np.exp(-x))

        @staticmethod
        def derivative(x):
            return ActivationFunction.Sigmoid.function(x) * (1 - ActivationFunction.Sigmoid.function(x))    

    class Tanh():
        
        @staticmethod
        def function(x):
            return np.tanh(x)

        @staticmethod
        def derivative(x):
            return 1 - np.tanh(x)**2  

    class ReLU():
        
        @staticmethod
        def function(x):
            return np.maximum(0, x)

        @staticmethod
        def derivative(x):
            return np.where(x <= 0, 0, 1)   

    class LeakyReLU():
        
        @staticmethod
        def function(x, alpha=0.01):
            return np.where(x > 0, x, x * alpha)

        @staticmethod
        def derivative(x, alpha=0.01):
            return np.where(x > 0, 1, alpha)       