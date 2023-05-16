import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np 
import ttkbootstrap as tb
import pandas as pd        

import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from ttkbootstrap.constants import *
import ttkbootstrap as tb
plt.style.use('dark_background')
root = tb.Window(themename="dracula")
root.title('Actuation Station')



fig = Figure(figsize=(4, 4), dpi = 200)
ax = fig.add_subplot(111)
ax.clear
ax.set_facecolor('#282a36')
x = np.linspace(0, 2*np.pi, 1000)
y = np.sin(x)
line, = ax.plot(x, y, color = '#bd93f9')
fig.patch.set_facecolor('#282a36')
ax.tick_params(color='#ffb86c', labelcolor='#ffb86c')
for spine in ax.spines.values():
        spine.set_edgecolor('#ffb86c')



label = tb.Label( text='Frequency:').pack(side=LEFT)

frequency = tb.Scale(value=1, from_=1, to=50,bootstyle="light")
frequency.pack(side=LEFT, fill=X, expand=YES, padx=5)

label2 = tb.Label(text='Amplitude:').pack(side=LEFT)

amplitude = tb.Scale(value=0.5, from_=0, to=10,bootstyle="light")
amplitude.pack(side=LEFT, fill=X, expand=YES, padx=5)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(expand=YES)
phase = 0

def update_plot():
    freq = frequency.get()
    amp = amplitude.get()
    line.set_ydata(amp * np.sin(freq * x + update_plot.i/10.0))
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.canvas.blit(ax.bbox)
    update_plot.i += 1

update_plot.i = 0

def start():
    if not animate.running:
        animate.running = True
        line.set_visible(True)
        animate()


def stop():
    animate.running = False 

def save():
    filename = name_entry.get()
    if filename:
        fig.savefig(filename + '.svg')    
def animate():
    if animate.running:
        update_plot()
        root.after(1, animate)   
animate.running = False         
start_label = tb.Button(root, text='Start', command= start,bootstyle="success-outline")
start_label.pack(side=LEFT,fill=X, expand=YES, padx=5)
stop_label = tb.Button(root, text='Stop', command= stop,bootstyle="warning-outline")
stop_label.pack(side = LEFT,fill=X, expand=YES, padx=5, )
label2 = tb.Label(text='File Name:').pack(side=LEFT)
name_entry = tb.Entry(root)
name_entry.pack(side = LEFT,fill=X, expand=YES, padx=5)

save_button = tb.Button(root, text="Save", command=save,bootstyle="danger-outline")
save_button.pack(fill=tk.X)
line.set_visible(False)
root.mainloop()