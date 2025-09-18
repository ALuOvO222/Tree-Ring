
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 年轮参数
NUM_RINGS = 30  # 年轮数量
MAX_RADIUS = 10  # 最大半径

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.axis('off')

# 生成每一圈的颜色和厚度
colors = plt.cm.terrain(np.linspace(0, 1, NUM_RINGS))
widths = np.linspace(0.2, 0.6, NUM_RINGS)

def draw_rings(frame):
	ax.clear()
	ax.set_aspect('equal')
	ax.axis('off')
	for i in range(frame):
		radius = (i + 1) * MAX_RADIUS / NUM_RINGS
		circle = plt.Circle((0, 0), radius, color=colors[i], fill=False, lw=8 * widths[i])
		ax.add_patch(circle)
	ax.set_xlim(-MAX_RADIUS - 1, MAX_RADIUS + 1)
	ax.set_ylim(-MAX_RADIUS - 1, MAX_RADIUS + 1)

ani = FuncAnimation(fig, draw_rings, frames=NUM_RINGS + 1, interval=200, repeat=False)

plt.show()
