import numpy as np
import matplotlib.pyplot as plt
import math 

freq = 5
n_waves = 20
colors = plt.cm.viridis(np.linspace(0, 1, n_waves))
x = np.linspace(0, 2 * np.pi, 300)
y = 2 * np.sin(freq * x)
amplitudes = np.linspace(0.1, 2, n_waves)

#for amplitude in np.linspace(0.5, 2, n_waves):
for j in range(n_waves): 
    amplitude = amplitudes[j]
    color = colors[j]
    y = amplitude * np.sin(freq * x)
    plt.plot(x,y, '-', color=color)

plt.xlim([0,2*np.pi])
plt.ylim([-2.25, 2.25])

#%%
import numpy as np
import matplotlib.pyplot as plt

n_bells = 50
resolution = 300
colors = plt.cm.Accent(np.linspace(0, 1, n_bells))
x = np.linspace(-3, 3, resolution)
amplitudes = np.linspace(0.1, 20, n_bells)
mu = 0
sigmas = np.linspace(0.1, 2, n_bells)

for k in range(n_bells):
    sigma = sigmas[k]
    amplitude = amplitudes[k]
    color = colors[k]
    y = amplitude * np.e ** -(((1/2) * x - mu) / (sigma)) ** 2
    plt.plot(x,y, '-', color=color)
