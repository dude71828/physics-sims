##import numpy as np
##from numpy import *
##import matplotlib.pyplot as plt
##import tkinter as tk
##from matplotlib import animation
##from matplotlib.widgets import Button, Slider
##import time
##
##
##
##thmin = 0
##thmax = 90
##t = np.linspace(0, 10, 1001)
##
##plt.style.use('dark_background')
##fig, ax = plt.subplots()
##fig.subplots_adjust(bottom=0.25)
##axth = fig.add_axes([0.25, 0.1, 0.65, 0.03])
##th_slider = Slider(
##    ax=axth,
##    label='Angle (degrees)',
##    valmin=thmin,
##    valmax=thmax,
##    valinit=(thmin+thmax)/2,
##)
##
##ax.set_xlim(0, 10)
##ax.set_ylim(thmin, thmax)
##
##th_user = np.zeros(len(t))
##th_gr, = plt.plot(t, th_user)
##
### The function to be called anytime a slider's value changes
##def slupdate(val):
##    th_user.insert(0, th_slider.val)
##    th_user.pop()
##    th_gr.set_ydata(th_user)
##    fig.canvas.draw_idle()
##
##
##for _ in range(len(t)):
##    slupdate()
##
##plt.show()


import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import *

DT_MS = 10
TOTAL_TIME = 5
N_SAMPLES = int(TOTAL_TIME * 1000 / DT_MS) + 1

th = []
t_vals = []

root = tk.Tk()
root.title("Slider Recorder")
root.geometry("400x150")

# --- slider ---
sl = tk.Scale(root, from_=0, to=90, orient=tk.HORIZONTAL, length=300, resolution=0.01)
sl.pack(pady=10)

# --- time label ---
time_label = tk.Label(root, text="Time: 0.000 s", font=("Arial", 12))
time_label.pack()

start_time = time.perf_counter()

def record():
    elapsed = time.perf_counter() - start_time

    th.append(sl.get())
    t_vals.append(elapsed)

    time_label.config(text=f"Time: {elapsed:6.3f} s")

    if len(th) < 501:
        root.after(10, record)
    else:
        root.destroy()

# start recording
root.after(0, record)
root.mainloop()

print("Samples recorded:", len(th))

plt.plot(np.linspace(0,5,501), th)
plt.show()

