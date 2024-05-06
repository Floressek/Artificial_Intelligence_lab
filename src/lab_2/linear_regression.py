import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Generowanie losowych danych
rand_value = np.random.randint(100)
np.random.seed(rand_value)
X = 2 * np.random.rand(1000, 1)
y = 4 + 3 * X + np.random.randn(1000, 1)

# Parametry inicjalizacyjne
learning_rate = 0.1
n_iterations = 1000
m = len(X)

# Inicjalizacja parametrów modelu (theta)
theta = np.random.randn(2, 1)

# Dodanie jedynki dla wyrazu wolnego (bias)
X_b = np.c_[np.ones((m, 1)), X]

# Implementacja spadku gradientu
for iteration in range(n_iterations):
    gradients = 2 / m * X_b.T.dot(X_b.dot(theta) - y)
    theta -= learning_rate * gradients

# Predykcje i MSE
predictions = X_b.dot(theta)
mse = ((predictions - y) ** 2).mean()
print("MSE:", mse)

# Obliczanie odległości od linii regresji
distances = np.abs(y - predictions)

# Normalizacja odległości dla kolorowania
norm = Normalize(vmin=np.min(distances), vmax=np.max(distances))
cmap = plt.get_cmap('RdYlGn_r')

# Rysowanie danych
fig, ax = plt.subplots()
scatter = ax.scatter(X, y, color=cmap(norm(distances)), edgecolor='k')

# Predykcja dla nowych wartości
X_new = np.array([[0], [2]])
X_new_b = np.c_[np.ones((2, 1)), X_new]
y_predict = X_new_b.dot(theta)

# Rysowanie linii regresji
ax.plot(X_new, y_predict, "b-", linewidth=2)

# Dodatki
ax.set_xlabel("Zmienna niezależna")
ax.set_ylabel("Zmienna zależna")
ax.set_title("Regresja liniowa z metodą spadku gradientu")
ax.legend(["Regresja liniowa"])
plt.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax, label='Odległość od linii regresji')

plt.show()
