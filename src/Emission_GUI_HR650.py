# Importing tkinter module
import tkinter as tk
from tkinter import filedialog
import numpy as np 
import ttkbootstrap as tb
import pandas as pd        
from HR640_Driver import HR640_Spectrometer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ttkbootstrap.constants import *
from time import sleep
from Helper_funcs import random_spectra , save_data, exp_auto_name
import time
import datetime
from datetime import date
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
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Intensity (Arb. Units.)')
ax.xaxis.label.set_color('#ffb86c')
ax.yaxis.label.set_color('#ffb86c')
ax.set_xlim(500,600)
ax.set_ylim(0,1000)
fig.tight_layout()
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
spectra = []  
start_time = None
stop_time = None

def get_save_direct():
    save_directory = filedialog.askdirectory()
    save_folder_var.set(save_directory)

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
      get_spectrometer_wl()
    else:
     status_var.set('Initialised')  
     get_spectrometer_wl()
    
def save():
    save_file = str(save_file_var.get())
    if save_file == '':
        save_file = exp_auto_name()
    else: 
        pass    
    print(save_file)
    save_folder = str(save_folder_var.get())
    print(save_folder)
    save_data(save_file,save_folder,start_time,stop_time)

       
def get_spectrometer_wl():
    global spectrometer
    wl = spectrometer.get_wavelength()   
    current_wl_var.set(wl)

def go_to_wavelength():
    go_to = go_to_var.get()
    global spectrometer
    if validate_number(go_to) == True:
        spectrometer.goto_wavelength(go_to)
        wl = spectrometer.get_wavelength()   
        current_wl_var.set(wl)
    else:
        pass    
def scan_range():
    global s_range
    s_range = None
    start_wl = start_var.get()
    stop_wl = stop_var.get()
    step_wl = step_var.get()
    if validate_number(start_wl) == True and validate_number(stop_wl) == True:
        s_range = np.arange(float(start_wl),float(stop_wl),float(step_wl))
    else:
        print('invalid inputs')    

def start():
        if scan.running == True: 
            pass 
        else:
            global interupt_type 
            global x_to_plot
            global y_to_plot
            global s_range
            global spectrometer 
            global spectra 
            global start_time
            scan_range()
            if spectrometer.emulation == True and interupt_type != 'pause':
                spectra = random_spectra(s_range)
            else: 
                pass    
            if interupt_type == 'stop' or interupt_type == 'finished':
                y_to_plot = []
                x_to_plot = []
                if not scan.running:
                    scan.running = True
                    start_time = str(datetime.datetime.now())
                    scan()
            elif interupt_type == 'pause':
                if not scan.running:     
                    scan.running = True
                    scan()   
            else:    
                if not scan.running:
                    scan.running = True
                    start_time = str(datetime.datetime.now())
                    scan()
        

def stop():
    global interupt_type
    global stop_time
    interupt_type = 'stop'
    scan.running = False 
    stop_time = str(datetime.datetime.now())
    save()

def pause():
    global interupt_type
    interupt_type = 'pause'
    scan.running = False 


def scan():
    global interupt_type
    global s_range
    global iterator
  
    if scan.i < len(s_range) and scan.running == True:

        spectrometer.goto_wavelength(s_range[iterator])
        update_plot()
        get_spectrometer_wl()
        scan.i += 1
        iterator += 1
        master.after(10, scan)  
    elif scan.running == False and interupt_type == 'stop':
        print('Scan stopped saving data regardless...')
        iterator = 0
        scan.i = 0

    elif scan.i < len(s_range) and interupt_type == 'pause':
        pass   

    else:
        global stop_time
        scan.running = False 
        interupt_type = 'finished'
        print('scan finished')
        stop_time = str(datetime.datetime.now())
        save()
        iterator = 0
        scan.i = 0

 

def update_plot():
    global s_range
    global x_to_plot 
    global y_to_plot

    x = s_range[iterator]
    y = spectra[iterator]
    x_to_plot.append(x)
    y_to_plot.append(y)
    line.set_ydata(y_to_plot)
    line.set_xdata(x_to_plot)
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.canvas.blit(ax.bbox) 
  

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

save_folder_var = tk.StringVar()  
save_folder_var.set('')

save_file_var = tk.StringVar()  
save_file_var.set('')

go_to_var = tk.StringVar(value='')
pane = tk.Frame(master)
pane.grid(row=0, column=0, padx=10, pady=5)
pane2 = tk.Frame(master)
pane2.grid(row=0, column=1, padx=10, pady=5)


# General layout of GUI

spec_init_button = tb.Button(pane, text='Initialise Spectrometer', command = get_spectrometer_status).grid(row=0, column=0, padx=5, pady=5)
spec_status_label = tb.Label(pane,textvariable=status_var,).grid(row=0, column=1, padx=5, pady=5)


spec_wl_button = tb.Label(pane, text='Current Wavelength:',).grid(row=1, column=0, padx=5, pady=5)
current_wl_label = tb.Label(pane,textvariable=current_wl_var,).grid(row=1, column=1, padx=5, pady=5)


spec_go_button = tb.Button(pane, text='Go to Wavelength', command = go_to_wavelength).grid(row=2, column=0, padx=5, pady=5)
go_to_entry = tb.Entry(pane, textvariable = go_to_var).grid(row=2, column=1, padx=5, pady=5)



start_params = tb.Label(pane,text='Start Wavelength',).grid(row=3, column=0, padx=5, pady=5)
start_entry = tb.Entry(pane, textvariable = start_var).grid(row=3, column=1, padx=5, pady=5)
stop_params = tb.Label(pane,text='Stop Wavelength',).grid(row=4, column=0, padx=5, pady=5)
stop_entry = tb.Entry(pane, textvariable = stop_var).grid(row=4, column=1, padx=5, pady=5)
step_params = tb.Label(pane,text='Step Size',).grid(row=5, column=0, padx=5, pady=5)
step_entry = tb.Entry(pane, textvariable = step_var).grid(row=5, column=1, padx=5, pady=5)
start_scan = tb.Button(pane, text='Start Scan',command = start ).grid(row=6, column=0, padx=5, pady=5)
stop_scan = tb.Button(pane, text='Stop Scan',command = stop).grid(row=6, column=1, padx=5, pady=5)
pause_scan = tb.Button(pane, text='Pause Scan',command = pause ).grid(row=7, column=0, padx=5, pady=5)

save_direct_button = tb.Button(pane, text='::', command = get_save_direct ).grid(row=8, column=3, padx=5, pady=5)
save_direct_label1 = tb.Label(pane,textvariable=save_folder_var).grid(row=8, column=1, padx=5, pady=5)
save_direct_label2 = tb.Label(pane,text = 'Save folder location:',).grid(row=8, column=0, padx=5, pady=5)
file_name_label = tb.Label(pane,text = 'Save file name:',).grid(row=9, column=0, padx=5, pady=5)
file_name_entry = tb.Entry(pane, textvariable = save_file_var,).grid(row=9, column=1, padx=5, pady=5)
"""""
Define Figure params
"""




canvas = FigureCanvasTkAgg(fig, master=pane2)
canvas.draw()
canvas.get_tk_widget().grid(row =7,column=1)
phase = 0
# Execute Tkinter
scan.i = 0  
scan.running = False   
master.mainloop()