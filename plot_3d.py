import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from mpl_toolkits.mplot3d.axes3d import get_test_data
import numpy as np
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
X, Y, Z = get_test_data(0.05)
C = np.linspace(-5, 5, Z.size).reshape(Z.shape)
scamap = plt.cm.ScalarMappable(cmap='inferno')
fcolors = scamap.to_rgba(C)
ax.plot_surface(X, Y, Z, facecolors=fcolors, cmap='inferno')
fig.colorbar(scamap)
plt.show()