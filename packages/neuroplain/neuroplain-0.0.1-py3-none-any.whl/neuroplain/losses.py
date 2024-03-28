import numpy as np

class LossFunction:

    class MSE():
        
        @staticmethod
        def function(y_true, y_pred):
            return np.mean((y_true - y_pred) ** 2)

        @staticmethod
        def derivative(y_true, y_pred):
            return 2 * (y_pred - y_true) / y_true.size


    class CrossEntropy():
            
        @staticmethod
        def function(y_true, y_pred):
            y_pred = np.clip(y_pred, 1e-12, 1 - 1e-12)
            return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

        @staticmethod
        def derivative(y_true, y_pred):
            y_pred = np.clip(y_pred, 1e-12, 1 - 1e-12)
            return -(y_true / y_pred) + (1 - y_true) / (1 - y_pred)