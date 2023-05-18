# Importing tkinter module
import tkinter as tk
import numpy as np 
import ttkbootstrap as tb
import pandas as pd        
from HR640_Driver import HR640_Spectrometer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ttkbootstrap.constants import *
from time import sleep


"""
Def Plot
"""
plt.style.use('dark_background')
fig = Figure(figsize=(4, 4), dpi = 200)
ax = fig.add_subplot(111)
ax.clear
ax.set_facecolor('#282a36')
x = 0
y = 0
ax.set_xlim(500,600)
ax.set_ylim(0,1000)
line, = ax.plot(x, y, color = '#bd93f9')
fig.patch.set_facecolor('#282a36')
ax.tick_params(color='#ffb86c', labelcolor='#ffb86c')
for spine in ax.spines.values():
        spine.set_edgecolor('#ffb86c')
"""
Global Vars
"""
spectrometer = None
lockin = None
s_range = None
iterator = 0 
y_to_plot = []
x_to_plot = []
interupt_type = None
def validate_number(x) -> bool:
    """Validates that the input is a number"""
    if x.isdigit():
        return True
    elif x == "":
        return False
    else:
        return False

def get_spectrometer_status():
    global spectrometer
    spectrometer = HR640_Spectrometer(emulate=True)
    if spectrometer.emulation == True:
      status_var.set('Emulated')
    else:
     status_var.set('Initialised')  
    
         
       
def get_spectrometer_wl():
    global spectrometer
    wl = spectrometer.get_wavelength()   
    current_wl_var.set(wl)

def go_to_wavelength():
    go_to = go_to_var.get()
    if validate_number(go_to) == True:
        spectrometer.goto_wavelength(go_to)
    else:
        pass    
def scan_range():
    global s_range
    s_range = None
    start_wl = start_var.get()
    stop_wl = stop_var.get()
    step_wl = step_var.get()
    if validate_number(start_wl) == True and validate_number(stop_wl) == True and validate_number(step_wl) == True:
        s_range = np.arange(float(start_wl),float(stop_wl),float(step_wl))
    else:
        print('invalid inputs')    

def start():
        global interupt_type 
        global x_to_plot
        global y_to_plot
        if interupt_type == 'stop':
            y_to_plot = []
            x_to_plot = []
        else:    
            if not scan.running:
                scan.running = True
                scan()
        

def stop():
    global interupt_type
    interupt_type = 'stop'
    scan.running = False 
    start_var.set('')
    stop_var.set('')
    step_var.set('')



def scan():
    try:
        scan_range()
        global s_range
        global iterator
        update_plot()
        if scan.i < len(s_range):
            if scan.running:
                
                scan.i += 1
                iterator += 1
                master.after(1000, scan)  
        else:
            scan.running = False 
            print('scan finished')
    except:
        scan.running = False   
        pass   
 

def update_plot():
    try:
        global s_range
        global x_to_plot
        global y_to_plot
    
        x = s_range[iterator]
        y = s_range[iterator]*1
        x_to_plot.append(x)
        y_to_plot.append(y)
        line.set_ydata(y_to_plot)
        line.set_xdata(x_to_plot)
        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        fig.canvas.blit(ax.bbox) 
    except:
        pass    

# creating Tk window and Tk Vars
master = tb.Window(themename="dracula")  
status_var = tk.StringVar()
status_var.set('Uninitialised')
current_wl_var = tk.StringVar()  
current_wl_var.set('')

start_var = tk.StringVar()  
start_var.set('')
stop_var = tk.StringVar()  
stop_var.set('')
step_var = tk.StringVar()  
step_var.set('')



go_to_var = tk.StringVar(value='')
pane = tk.Frame(master)
pane.grid(row=0, column=0, padx=10, pady=5)
pane2 = tk.Frame(master)
pane2.grid(row=0, column=1, padx=10, pady=5)


# General layout of GUI

spec_init_button = tb.Button(pane, text='Initialise Spectrometer', command = get_spectrometer_status).grid(row=0, column=0, padx=5, pady=5)
spec_status_label = tb.Label(pane,textvariable=status_var,).grid(row=0, column=1, padx=5, pady=5)


spec_wl_button = tb.Button(pane, text='Get Current Wavelength', command = get_spectrometer_wl).grid(row=1, column=0, padx=5, pady=5)
current_wl_label = tb.Label(pane,textvariable=current_wl_var,).grid(row=1, column=1, padx=5, pady=5)


spec_go_button = tb.Button(pane, text='Go to Wavelength', command = go_to_wavelength).grid(row=2, column=0, padx=5, pady=5)
go_to_entry = tb.Entry(pane, textvariable = go_to_var).grid(row=2, column=1, padx=5, pady=5)


start_scan = tb.Button(pane, text='Start Scan',command = start ).grid(row=6, column=0, padx=5, pady=5)
stop_scan = tb.Button(pane, text='Stop Scan',command = stop).grid(row=6, column=1, padx=5, pady=5)
start_params = tb.Label(pane,text='Start Wavelength',).grid(row=3, column=0, padx=5, pady=5)
start_entry = tb.Entry(pane, textvariable = start_var).grid(row=3, column=1, padx=5, pady=5)
stop_params = tb.Label(pane,text='Stop Wavelength',).grid(row=4, column=0, padx=5, pady=5)
stop_entry = tb.Entry(pane, textvariable = stop_var).grid(row=4, column=1, padx=5, pady=5)
step_params = tb.Label(pane,text='Step Size',).grid(row=5, column=0, padx=5, pady=5)
step_entry = tb.Entry(pane, textvariable = step_var).grid(row=5, column=1, padx=5, pady=5)
"""
Define Figure params
"""



canvas = FigureCanvasTkAgg(fig, master=pane2)
canvas.draw()
canvas.get_tk_widget().grid(row =7)
phase = 0
# Execute Tkinter
scan.i = 0  
scan.running = False   
master.mainloop()