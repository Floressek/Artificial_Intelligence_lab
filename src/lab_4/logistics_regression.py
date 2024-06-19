import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification


# Function to calculate the sigmoid of a given input
def _sigmoid(x):
    """Calculate the sigmoid of x.

    Args:
        x (float): Input value.

    Returns:
        float: The sigmoid of x.
    """
    return 1 / (1 + np.exp(-x))


# Function to compute the loss between the true and predicted values
def compute_loss(y_true, y_pred):
    """Compute the loss between the true and predicted values.

    Args:
        y_true (array-like): Array of true values.
        y_pred (array-like): Array of predicted values.

    Returns:
        float: The computed loss.
    """
    epsilon = 1e-9
    y1 = y_true * np.log(y_pred + epsilon)
    y2 = (1 - y_true) * np.log(1 - y_pred + epsilon)
    return -np.mean(y1 + y2)


# Logistic Regression class
class LogisticRegression:
    """Logistic Regression Classifier.

    Attributes:
        learning_rate (float): Learning rate for the gradient descent optimization. Defaults to 0.2.
        n_iters (int): Number of iterations for the gradient descent optimization. Defaults to 100000.
        weights (ndarray): Weights after fitting the model. Initialized to None.
        bias (float): Bias after fitting the model. Initialized to None.
        losses (list): List of loss values computed during the training. Initialized to an empty list.
    """

    def __init__(self, learning_rate=0.2, n_iters=100000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None
        self.losses = []

    def fit(self, X, y):
        """Fit the model according to the given training data.

        Args:
            X (array-like): Training data.
            y (array-like): Target values.

        Returns:
            self: Returns an instance of self.
        """
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            A = _sigmoid(np.dot(X, self.weights) + self.bias)
            self.losses.append(compute_loss(y, A))
            dz = A - y
            dw = (1 / n_samples) * np.dot(X.T, dz)
            db = (1 / n_samples) * np.sum(dz)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        """Predict class labels for samples in X.

        Args:
            X (array-like): Samples.

        Returns:
            array-like: Predicted class label per sample.
        """
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = _sigmoid(linear_output)
        return [1 if i > 0.5 else 0 for i in y_predicted]

    def plot_decision_boundary(self, X, y):
        """Plot the decision boundary of the Logistic Regression model.

        Args:
            X (array-like): Training data.
            y (array-like): Target values.
        """
        # Setting limits and grid
        x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1

        # Generating a grid of values
        xx1, xx2 = np.meshgrid(np.linspace(x1_min, x1_max, 800),  # Increased from 100 to 500
                               np.linspace(x2_min, x2_max, 800))

        # Predicting values across the grid
        grid = np.c_[xx1.ravel(), xx2.ravel()]
        pred_func = self.predict(grid)
        Z = np.array(pred_func).reshape(xx1.shape)

        # Plotting the contour and training examples
        plt.contourf(xx1, xx2, Z, alpha=0.5, cmap="Wistia_r")
        plt.scatter(X[:, 0], X[:, 1], c=y, cmap="Wistia_r", s=40, edgecolor='k')
        plt.title("Decision Boundary for Logistic Regression")
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")
        plt.show()


# Generating synthetic data
X, y = make_classification(n_features=2, n_redundant=0, n_clusters_per_class=2, n_samples=200)
model = LogisticRegression()
model.fit(X, y)

# Plotting the decision boundary
model.plot_decision_boundary(X, y)
