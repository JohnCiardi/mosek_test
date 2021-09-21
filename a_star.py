import numpy as np
import matplotlib.pyplot as plt

fig1 = plt.figure("sphere points 1")
ax1 = fig1.add_subplot(111,projection='3d')

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 50)

x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax1.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)

#生成散点图
ax1.scatter(x,y,z)
plt.grid()
plt.show()
