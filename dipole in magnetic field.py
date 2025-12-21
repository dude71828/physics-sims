import numpy as np
import sympy as smp
import matplotlib.pyplot as plt
from numpy import linspace, meshgrid, sqrt, sin, cos, pi
from scipy.integrate import odeint, RK45, solve_ivp
from matplotlib import animation, colors, colormaps
from matplotlib.collections import LineCollection

FPS = 75
SIM_LEN = 10
pltsize = 10
speed = 1
trlen = 60

q = 1
m = 1
d = 1
B = 1
c1 = q*B/m
c2 = c1*d/2
c3 = c1*2/d

vx0 = 1
vy0 = -2
omg0 = 0.5

saved = 1

t = np.linspace(0, SIM_LEN, SIM_LEN*FPS+1)

def func(t, S):
    th, th_d, vx, vy, x, y = S
    dth = th_d
    dth_d = - c3 * (vx * np.cos(th)  + vy * np.sin(th))
    dvx = c2 * th_d * np.cos(th)
    dvy = c2 * th_d * np.sin(th)
    dx = vx
    dy = vy
    return (dth, dth_d, dvx, dvy, dx, dy)

sol = solve_ivp(
    func,
    (0, SIM_LEN),
    y0=(0, omg0, vx0, vy0, 0, 0),
    t_eval=t,
    method='RK45'
)

thf = sol.y[0]
th_df = sol.y[1]
vxf = sol.y[2]
vyf = sol.y[3]
xf = sol.y[4]
yf = sol.y[5]


charge1x_raw = xf + d/2 * np.cos(thf)
charge1y_raw = yf + d/2 * np.sin(thf)

charge2x_raw = xf - d/2 * np.cos(thf)
charge2y_raw = yf - d/2 * np.sin(thf)


charge1x = [charge1x_raw[i] for i in range(SIM_LEN*FPS+1) if i % speed == 0]
charge1y = [charge1y_raw[i] for i in range(SIM_LEN*FPS+1) if i % speed == 0]

charge2x = [charge2x_raw[i] for i in range(SIM_LEN*FPS+1) if i % speed == 0]
charge2y = [charge2y_raw[i] for i in range(SIM_LEN*FPS+1) if i % speed == 0]

plt.style.use('dark_background')
fig, ax = plt.subplots()
ax.set_xlim([-pltsize,pltsize])
ax.set_ylim([-pltsize,pltsize])
ax.set_aspect("equal")

trail1, = ax.plot([],[], lw=8/pltsize, color='r', alpha=0.5)
trail2, = ax.plot([],[], lw=8/pltsize, color='c', alpha=0.5)
ani_line, = ax.plot([], [], lw=8/pltsize, color='w')
ani_c1, = ax.plot([], [], 'o', ms=56/pltsize, color='r')
ani_c2, = ax.plot([], [], 'o', ms=56/pltsize, color='c')



def update(frame):
    x1 = charge1x[frame]
    y1 = charge1y[frame]
    x2 = charge2x[frame]
    y2 = charge2y[frame]
    
    ani_c1.set_data([x1],[y1])
    ani_c2.set_data([x2],[y2])
    ani_line.set_data([x1,x2], [y1,y2])

    i = max(0, frame-trlen)
    trail1.set_data(charge1x[i:frame], charge1y[i:frame])
    trail2.set_data(charge2x[i:frame], charge2y[i:frame])

    return trail1, trail2, ani_line, ani_c1, ani_c2

ani = animation.FuncAnimation(
    fig=fig,
    func=update,
    frames=len(charge1x),
    interval=40,
    repeat=True,
    blit=False
)


if saved:
    ani.save("dipole.gif")
else:
    plt.show()
