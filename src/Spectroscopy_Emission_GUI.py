# Importing tkinter module
import tkinter as tk
from tkinter import filedialog
import numpy as np 
import ttkbootstrap as tb
import pandas as pd        
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ttkbootstrap.constants import *
from time import sleep
from Helper_funcs import random_spectra , save_data, exp_auto_name, data_prep, make_config
import time
import datetime
from datetime import date
import os
import toml
import importlib
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
ax.set_xlim(500,520)
ax.set_ylim(0,20)
fig.tight_layout()
line, = ax.plot(x, y, color = '#bd93f9')
fig.patch.set_facecolor('#282a36')
ax.tick_params(color='#ffb86c', labelcolor='#ffb86c')
for spine in ax.spines.values():
        spine.set_edgecolor('#ffb86c')
"""
Global Vars
"""
emulation_status = False
multi_connect_status = False
daq = None
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
init_graph = None
config_file = None
config_toml = None
connected_devices = []


SUPPORTING_INSTRUMENT_DRIVERS = {
    'Laser': ('Laser_Driver', 'LaserDriver'),
    'PowerMeter': ('PowerMeter_Driver', 'PowerMeterDriver'),
    'SP_Instrument': ('Simulated_Support_Driver', 'Test_Support')

}

SPECTROMETER_DRIVERS = {
    'HR640': ('HR640_Driver', 'HR640_Spectrometer'),
    'iHR550': ('IHR550_Driver', 'IHR550_Spectrometer'),
    # Add other spectrometers here
}


DAQ_DRIVERS = {'simulated daq': ('Simulated_Daq_Driver', 'Test_Daq'),
               'SDS2352X-E': ('SIGLENT_Driver', 'SiglentSDS2352XE')} 
# functions that make the GUI work 

def spectrometer_dropdown(e):
    global spectrometer
    if scan.running == True: 
        pass 
    else:
        print(f'you selected {spectrometer_select.get()}')
        spectrometer = spectrometer_select.get()

def daq_dropdown(e):
    global daq
    print(f'you selected {daq_select.get()}')
    daq = daq_select.get()

def get_save_direct():
    save_directory = filedialog.askdirectory()
    save_folder_var.set(save_directory)

def get_config_file():
    global config_file
    global daq
    config_file = filedialog.askopenfilename()
    config_file_base_name = os.path.basename(config_file)
    config_file_var.set(config_file_base_name)
    load_config(config_file)
    if status_var == 'Initialised' or 'Emulated':
       daq = None
       status_var.set('Uninitialised')


def load_config(path: str) -> dict:
    global config_toml
    with open(path, 'r') as f:
        config_toml = toml.load(f)
  

def validate_number(x) -> bool:
    """Validates that the input is a number"""
    try:
        float(x)
        return True
    except ValueError:
        return False




def instrument_init():
    global spectrometer
    global emulation_status
    global daq
    global config_toml 
    global connected_devices

    match config_toml:
        case None:
            print('No config file loaded')
            return
        
    match spectrometer:
        case spectrometer if spectrometer in SPECTROMETER_DRIVERS:
        
            module_name, class_name = SPECTROMETER_DRIVERS[spectrometer]
      
            module = importlib.import_module(module_name)
         
            DriverClass = getattr(module, class_name)
      
            spectrometer = DriverClass(emulate=emulation_status)
            get_spectrometer_wl()
            connected_devices.append(spectrometer.name)  
        case _:
            print(f'Unknown spectrometer: {spectrometer}') 

    match daq:

        case daq if daq in DAQ_DRIVERS:
                
                    module_name, class_name = DAQ_DRIVERS[daq]
            
                    module = importlib.import_module(module_name)
          
                    DriverClass = getattr(module, class_name)
            
                    daq = DriverClass(config_toml, emulate=emulation_status)
                    
                    connected_devices.append(daq.name)  
        case _:
            print(f'Unknown daq: {daq}')
    if multi_connect_status == True:   
        print('loading multiple devices')     
        ignored_devices = set(DAQ_DRIVERS.keys()).union(SPECTROMETER_DRIVERS.keys())
        
        for device, device_info in config_toml.items():
     
            if device in ignored_devices:
                continue

          
            if device in SUPPORTING_INSTRUMENT_DRIVERS:
                
          
                module_name, class_name = SUPPORTING_INSTRUMENT_DRIVERS[device]
    
                module = importlib.import_module(module_name)

                DriverClass = getattr(module, class_name)

                
                instrument = DriverClass(config_toml)

            
                connected_devices.append(instrument.name) 

    print(f'connected devices: {connected_devices} ')
    if emulation_status == True:
        status_var.set('Emulated')
    else:
        status_var.set('Initialised')             
                


                       
    



def save():
    global x_to_plot
    global y_to_plot
    global s_range
    global config_toml
    start_wl = start_var.get()
    stop_wl = stop_var.get()
    step_wl = step_var.get()
    data_points = len(s_range)
    config_range = start_wl + '-' + stop_wl + ' nm'
    results = data_prep({'Amplitude': y_to_plot , 'Wavelength': x_to_plot})

    save_file = str(save_file_var.get())
    if save_file == '':
        save_file = exp_auto_name()
    else: 
        pass    
    print(save_file)
    save_folder = str(save_folder_var.get())
    print(save_folder)
    config = make_config(spectrometer, config_range, step_wl, data_points, config_toml, connected_devices)
    save_data(save_file, save_folder, start_time, stop_time, results, config)

       
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
        elif status_var.get() == 'Uninitialised':
            print('Devices not initialised')
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
            elif spectrometer.emulation == False and interupt_type != 'pause': 
                spectra = np.zeros(len(s_range))
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
    if scan.running == False: 
        pass 
    else:
        global interupt_type
        global stop_time
        global init_graph
        interupt_type = 'stop'
        init_graph = 'yes'
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
    global init_graph
  
    if scan.i < len(s_range) and scan.running == True:
        # this is tempory logic why it is been developed out of the lab. 
        spectrometer.goto_wavelength(s_range[iterator])
        if spectrometer.emulation == True and daq.name == 'simulated daq':
            spectra[iterator]= daq.measure()
        elif spectrometer.emulation == True and daq.name != 'simulated daq':
            spectra[iterator]= daq.measure()
        else: 
             pass
             #spectra[iterator]= daq.measure()   
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
        init_graph = 'yes'
        print('scan finished')
        stop_time = str(datetime.datetime.now())
        save()
        iterator = 0
        scan.i = 0

 

def update_plot():
    global s_range
    global x_to_plot 
    global y_to_plot
    global interupt_type
    global init_graph 
    global spectra
    x = s_range[iterator]
    y = spectra[iterator]

    # Check if x or y is outside the current plot range
    if init_graph == None or init_graph == "yes":
        new_x_limits = [x, x + 20]
        new_y_limits = [y, y + 20]

        ax.set_xlim(new_x_limits)
        ax.set_ylim(new_y_limits)

        # Update x-axis labels
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_text(str(int(tick.get_loc())))

        # Update y-axis labels
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_text(str(int(tick.get_loc())))  

        ax.figure.canvas.draw_idle()
        ax.figure.canvas.flush_events()  
        init_graph = "no"  

    x_limits = np.array(ax.get_xlim())
    y_limits = np.array(ax.get_ylim())
    update_x_higher = x > x_limits[1]
    update_y = y > y_limits[1]


    
    if update_x_higher and update_y:
        # Update the plot limits
        new_x_limits = [x_limits[0], max(x_limits[1], x + 20)] if update_x_higher else x_limits
        new_y_limits = [y_limits[0], max(y_limits[1], y + 20)] if update_y else y_limits

        ax.set_xlim(new_x_limits)
        ax.set_ylim(new_y_limits)

        # Update x-axis labels
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_text(str(int(tick.get_loc())))

        # Update y-axis labels
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_text(str(int(tick.get_loc())))

        # Draw the figure idle to update the plot and labels
        ax.figure.canvas.draw_idle()
        ax.figure.canvas.flush_events()

    if update_y: 
        new_y_limits = [y_limits[0], max(y_limits[1], y + 20)] if update_y else y_limits
        ax.set_ylim(new_y_limits)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_text(str(int(tick.get_loc())))

        ax.figure.canvas.draw_idle()
        ax.figure.canvas.flush_events()

    if update_x_higher:
        new_x_limits = [x_limits[0], max(x_limits[1], x + 20)] if update_x_higher else x_limits
        ax.set_xlim(new_x_limits)
        # Update x-axis labels
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_text(str(int(tick.get_loc())))

        # Draw the figure idle to update the plot and labels
        ax.figure.canvas.draw_idle()
        ax.figure.canvas.flush_events()


    x_to_plot.append(x)
    y_to_plot.append(y)
    line.set_ydata(y_to_plot)
    line.set_xdata(x_to_plot)
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.canvas.blit(ax.bbox) 
  

# creating Tk window and Tk Vars
theme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'theme.json'))
style = tb.Style()
style.load_user_themes(theme_path)
style.theme_use('dracula')
master = style.master
master.wm_title("SPECTRE Emission GUI")
 




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

config_file_var = tk.StringVar()  
config_file_var.set('')

save_file_var = tk.StringVar()  
save_file_var.set('')

def getBool(): 
    global emulation_status
    global multi_connect_status
    emulation_status = boolvar_emulation.get()
    multi_connect_status = boolvar_multi.get()

boolvar_emulation =tk.BooleanVar()
boolvar_emulation.set(False)

boolvar_multi =tk.BooleanVar()
boolvar_multi.set(False)

go_to_var = tk.StringVar(value='')
pane = tk.Frame(master)
pane.grid(row=0, column=0, padx=10, pady=5)
pane2 = tk.Frame(master)
pane2.grid(row=0, column=1, padx=10, pady=5)


# General layout of GUI
spectrometers = ['HR640', 'iHR550']
daqs = ['SDS2352X-E', 'Tektronix Scope', 'C8855-01 Photon counter', 'lock-in', 'simulated daq']

config_direct_button = tb.Button(pane, text='::', command = get_config_file ).grid(row=1, column=3, padx=5, pady=5)
config_direct_label1 = tb.Label(pane,textvariable=config_file_var).grid(row=1, column=1, padx=5, pady=5)
config_direct_label2 = tb.Label(pane,text = 'Config file loaded:',).grid(row=1, column=0, padx=5, pady=5)

spectrometer_label = tb.Label(pane,text='Spectrometer',).grid(row=2, column=0, padx=5, pady=5)
daq_label = tb.Label(pane,text='Signal source',).grid(row=2, column=1, padx=5, pady=5)
spectrometer_select = tb.Combobox(pane, values = spectrometers)
spectrometer_select.grid(row=3, column=0,padx=5, pady=5)
spectrometer_select.bind("<<ComboboxSelected>>",spectrometer_dropdown)
daq_select = tb.Combobox(pane, values = daqs)
daq_select.grid(row=3, column=1, padx=5, pady=5)
daq_select.bind("<<ComboboxSelected>>",daq_dropdown)

init_button = tb.Button(pane, text='Initialise', command = instrument_init).grid(row=4, column=0, padx=5, pady=5)
spec_status_label = tb.Label(pane,textvariable=status_var,).grid(row=4, column=1, padx=5, pady=5)
emulate_button = tb.Checkbutton(pane, text = "Emulate", variable = boolvar_emulation, command = getBool).grid(row=0, column=0, padx=5, pady=5)
multiconnect_button = tb.Checkbutton(pane, text = "Multi-connect", variable = boolvar_multi, command = getBool).grid(row=0, column=1, padx=5, pady=5)

spec_wl_button = tb.Label(pane, text='Current Wavelength:',).grid(row=5, column=0, padx=5, pady=5)
current_wl_label = tb.Label(pane,textvariable=current_wl_var,).grid(row=5, column=1, padx=5, pady=5)


spec_go_button = tb.Button(pane, text='Go to Wavelength', command = go_to_wavelength).grid(row=6, column=0, padx=5, pady=5)
go_to_entry = tb.Entry(pane, textvariable = go_to_var).grid(row=6, column=1, padx=5, pady=5)



start_params = tb.Label(pane,text='Start Wavelength',).grid(row=7, column=0, padx=5, pady=5)
start_entry = tb.Entry(pane, textvariable = start_var).grid(row=7, column=1, padx=5, pady=5)
stop_params = tb.Label(pane,text='Stop Wavelength',).grid(row=8, column=0, padx=5, pady=5)
stop_entry = tb.Entry(pane, textvariable = stop_var).grid(row=8, column=1, padx=5, pady=5)
step_params = tb.Label(pane,text='Step Size',).grid(row=9, column=0, padx=5, pady=5)
step_entry = tb.Entry(pane, textvariable = step_var).grid(row=9, column=1, padx=5, pady=5)
start_scan = tb.Button(pane, text='Start Scan',command = start ).grid(row=10, column=0, padx=5, pady=5)
stop_scan = tb.Button(pane, text='Stop Scan',command = stop).grid(row=10, column=1, padx=5, pady=5)
pause_scan = tb.Button(pane, text='Pause Scan',command = pause ).grid(row=11, column=0, padx=5, pady=5)

save_direct_button = tb.Button(pane, text='::', command = get_save_direct ).grid(row=12, column=3, padx=5, pady=5)
save_direct_label1 = tb.Label(pane,textvariable=save_folder_var).grid(row=12, column=1, padx=5, pady=5)
save_direct_label2 = tb.Label(pane,text = 'Save folder location:',).grid(row=12, column=0, padx=5, pady=5)
file_name_label = tb.Label(pane,text = 'Save file name:',).grid(row=13, column=0, padx=5, pady=5)
file_name_entry = tb.Entry(pane, textvariable = save_file_var,).grid(row=13, column=1, padx=5, pady=5)




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