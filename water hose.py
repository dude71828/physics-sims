import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib import animation
from matplotlib.widgets import Button, Slider
import time
import imageio_ffmpeg

dt = 0.01
t_tot = 10
fr_tot = int(t_tot/dt)+1
pi = np.pi
pltsize = (13, 13)

v = 12
g = 10
thmin = 0
thmax = 90
thinit = (thmin+thmax)/2

sliderd = 1
saved = 1

t = np.linspace(0, t_tot, fr_tot)


#-----------slider/func-----------
if sliderd:
    root = tk.Tk()
    root.title("Slider Top 10")
    root.geometry("400x150")

    sl = tk.Scale(root, from_=thmin, to=thmax, orient=tk.HORIZONTAL, length=300, resolution=0.01)
    sl.set(thinit)
    sl.pack()

    time_label = tk.Label(root, text="Time: 0.000 s", font=("Arial", 12))
    time_label.pack()

    start_time = time.perf_counter()
    th_user = []

    def record():
            elapsed = time.perf_counter() - start_time

            th_user.append(sl.get())

            time_label.config(text=f"Time: {elapsed:6.3f} s")

            if len(th_user) < fr_tot:
                    root.after(6, record)
            else:
                    root.destroy()

    root.after(0, record)
    root.mainloop()

else:
    th_user = 15 * np.sin(2 * pi * 0.6 * t) + 60

#-----------plotting-----------
th = np.array(th_user)*pi/180

plt.style.use('dark_background')
plt.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
fig, ax = plt.subplots(1, 2, figsize=(10,10))


ax[0].set_xlim(0, pltsize[0])
ax[0].set_ylim(0, pltsize[1])

x_plot = np.linspace(0,pltsize[0], fr_tot)
envelope = -g/(2*v**2)*x_plot**2+v**2/(2*g)
ax[0].axis("scaled")
ax[0].grid(alpha=0.5)
ax[0].set_box_aspect(1)
ax[0].autoscale(False)

ax[0].plot(x_plot, envelope, color='w', alpha=0.5)
curve, = ax[0].plot([], [])

ax[0].set_xlabel('x(m)')
ax[0].set_ylabel('y(m)')

usergr, = ax[1].plot([], [])
ax[1].set_xlim(0, t_tot)
ax[1].set_ylim(0, 90)
ax[1].set_box_aspect(1)

ax[1].set_xlabel('t(s)')
ax[1].set_ylabel('User θ(°)')

plt.tight_layout()

def update(frame):
    th_list = th[:frame+1]
    t_list = t[:frame+1]
    x = []
    y = []
    for i in range(frame+1):
        t_pt = (frame-i)*dt
        y_pt = v * t_pt * np.sin(th_list[i]) - 0.5 * g * t_pt**2
        x_pt = v * t_pt * np.cos(th_list[i])
        x.append(x_pt)
        y.append(y_pt)
        
    curve.set_data(x, y)
    usergr.set_data(t_list, th_user[:frame+1])

    return curve, usergr

anim = animation.FuncAnimation(
    fig,
    update,
    frames=fr_tot,
    interval=1000*dt,
    repeat=False
)

if saved:
    anim.save("water.mp4")
else:
    plt.show()

