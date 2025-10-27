import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams.update({'font.size': 22})
COLOR = 'white'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
# mpl.rcParams['font.family'] = 'monospace'
y, x = np.meshgrid(np.linspace(0, 10, 200), np.linspace(0, 10, 200))
p = np.exp(-x**2)
q = np.exp(-y**2)
# q = 1 / (1 + y**2)

# z = (p - q) * y / (1 + y**2)
z = (p - q) * y
# z = p * np.log2 (p / q)

fig, ax = plt.subplots()
from matplotlib import font_manager

font_path = '/Users/richard/Library/Fonts/JetBrainsMono-Regular.ttf'  # Your font path goes here
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()

c = ax.pcolormesh(x, y, z, cmap='jet')
ax.set_title('Gradient of SNE')
ax.axis([x.min(), x.max(), y.min(), y.max()])

fig.colorbar(c, ax=ax)
fig.patch.set_facecolor('black')
ax.set_xlabel('High-dimensional distance')
ax.set_ylabel('Low-dimensional distance')

plt.show()
