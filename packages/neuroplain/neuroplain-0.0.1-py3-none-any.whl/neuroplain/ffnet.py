import numpy as np

class FFNetwork:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_derivative = None
        self.initial_learning_rate = 0.01
        self.learning_rate = self.initial_learning_rate
        self.learning_rate_decay = False
        self.decay_rate = 0.1
        self.decay_steps = 100
        
    def add_layer(self, layer):
        self.layers.append(layer)

    def forward(self, input_data):
        for layer in self.layers:
            input_data = layer.forward(input_data)
        return input_data

    def backward(self, loss_gradient, learning_rate):
        for layer in reversed(self.layers):
            loss_gradient = layer.backward(loss_gradient, learning_rate)

    def set_loss_function(self, lossfunction):
        self.loss = lossfunction.function
        self.loss_derivative = lossfunction.derivative

    def set_learning_rate_decay(self,decay, decay_rate=0.1, decay_steps=100):
        self.learning_rate_decay = decay
        self.decay_rate = decay_rate
        self.decay_steps = decay_steps


    def train(self, X_train, y_train, epochs, learning_rate):
        self.initial_learning_rate = learning_rate        
        self.learning_rate = learning_rate        
        if y_train.shape[0] != X_train.shape[0]:
            y_train = y_train.T
        for epoch in range(epochs):
            total_loss = 0
            for x, y in zip(X_train, y_train):
                output = self.forward(x.reshape(-1, 1))
                total_loss += self.loss(y.reshape(-1, 1), output)
                loss_grad = self.loss_derivative(y.reshape(-1, 1), output)
                self.backward(loss_grad, learning_rate)
                
            if self.learning_rate_decay and (epoch + 1) % self.decay_steps == 0:
                self.learning_rate *= self.decay_rate  
                      
            average_loss = total_loss / len(X_train)
            print(f'Epoch {epoch+1}, Loss: {average_loss}, Learning Rate: {self.learning_rate}')


    def predict(self, input_data):
        return self.forward(input_data.reshape(-1, 1))


    def split_dataset(self, X, y, validation_split=0.2):
        if not 0 < validation_split < 1:
            raise ValueError("validation_split must be between 0 and 1")
        n_samples = X.shape[0]
        indices = np.arange(n_samples)
        np.random.shuffle(indices)
        X, y = X[indices,:], y[indices]
        split_idx = int(n_samples * (1 - validation_split))
        X_train, X_val = X[:split_idx,:], X[split_idx:,:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        return X_train, y_train, X_val, y_val    