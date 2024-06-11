# Python program to Plot Perfect Heart Shape

# importing libraries
import numpy as np
from matplotlib import pyplot as plt

# Creating equally spaced 100 data in range 0 to 2*pi
theta = np.linspace(0, 2 * np.pi, 100)

# Generating x and y data
#x = 16 * ( np.sin(theta) ** 3 )
x = 16 * ( np.sin(theta) ** 3 )
#y = 13 * np.cos(theta) - 5* np.cos(2*theta) - 2 * np.cos(3*theta) - np.cos(4*theta)
y = 13 * np.cos(theta) - 5* np.cos(2*theta) - 2 * np.cos(3*theta) - np.cos(4*theta)

# Plotting
plt.plot(x, y)
plt.title('Heart Shape')
plt.show()
input(Block=True)