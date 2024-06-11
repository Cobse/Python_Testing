# Python program to Plot Perfect Heart Shape

# importing libraries
import numpy as np
from matplotlib import pyplot as plt

# Generating x and y data
x = np.linspace(-2, 2, 1000)
y = np.linspace(-2, 2, 1000)

X, Y = np.meshgrid(x, y)
Z = (X**2 + Y**2 - 1)**3 - X**2 * Y**3

# Plotting
plt.contour(X, Y, Z, [0], colors='red')  # Plotting the contour at Z = 0
plt.title('Heart Shape')
plt.axis('scaled')
plt.show(block=True)
