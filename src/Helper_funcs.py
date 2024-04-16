import numpy as np
import random as rd
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import time
import datetime
from datetime import date
import pandas as pd

def Gamma2sigma(Gamma):
    '''Function to convert FWHM (Gamma) to standard deviation (sigma) for stats.norm'''
    return Gamma * np.sqrt(2) / ( np.sqrt(2 * np.log(2)) * 2 )

def random_spectra(X):
    #generates a random spectra (optimised for nm) for the scaned wavelength range. Generates 5 peaks, though they may not be resolved
    sigma1 = Gamma2sigma(rd.uniform(0.1, 10)) 
    sigma2 = Gamma2sigma(rd.uniform(0.1, 10)) 
    sigma3 = Gamma2sigma(rd.uniform(0.1, 10)) 
    sigma4 = Gamma2sigma(rd.uniform(0.1, 10)) 
    sigma5 = Gamma2sigma(rd.uniform(0.1, 10)) 


    LINE1 = stats.norm.pdf(X,rd.uniform(np.min(X)+10,np.max(X)-10), sigma1) * 1000
    LINE2 = stats.norm.pdf(X,rd.uniform(np.min(X)+10,np.max(X)-10), sigma2) * 1000 
    LINE3 = stats.norm.pdf(X,rd.uniform(np.min(X)+10,np.max(X)-10), sigma3) * 1000
    LINE4 = stats.norm.pdf(X,rd.uniform(np.min(X)+10,np.max(X)-10), sigma4) * 1000 
    LINE5 = stats.norm.pdf(X,rd.uniform(np.min(X)+10,np.max(X)-10), sigma5) * 1000
    LINE_TOT = LINE1 + LINE2 + LINE3 + LINE4 + LINE5
    return LINE_TOT

def name_checker(fname_path):
    """
    Get the path to a filename which does not exist by incrementing path.

    Examples
    --------
    >>> get_nonexistant_path('/etc/issue')
    '/etc/issue-1'
    >>> get_nonexistant_path('whatever/1337bla.py')
    'whatever/1337bla.py'
    """
    if not os.path.exists(fname_path):
        return os.path.basename(fname_path)
    filename, file_extension = os.path.splitext(fname_path)
    i = 1
    new_fname = "{}-{}{}".format(filename, i, file_extension)
    while os.path.exists(new_fname):
        i += 1
        new_fname = "{}-{}{}".format(filename, i, file_extension)
    return  os.path.basename(new_fname) 

def exp_auto_name():
    now = datetime.datetime.now()
    now_str = str(now)
    substitutions = [
        (":", "_"),
        (".", "_"),
        (" ", "_"),
        ("-", "_")]

    for search, replacement in substitutions:
        now_str = now_str.replace(search, replacement)    
    experiment_name = 'experiment_' + now_str
    return experiment_name

def make_config(spectrometer, scan_range, steps, number_data_points, config_toml, connected_devices):
    spectrometer_name = spectrometer.name
    print(config_toml.items())
    config = ''
    config += 'Emulated measurement?: ' + str("{}").format(spectrometer.emulation) + '\n'
    config += 'Spectrometer: ' + spectrometer_name + '\n'
    config += 'Scan range:  ' + scan_range + '\n'
    config += 'Step size: ' + steps + '\n'
    config += 'Number of data points: ' + str(number_data_points) + '\n\n' 
    config += config_toml_iter(config_toml, connected_devices)
    config += '\n'
    return config

def config_toml_iter(config_toml: dict, connected_devices: list) -> str:
    '''
    Take the loaded config toml file and iterate through it, returning lines of strings of the config file
    '''

    
    config_temp = ''
    for device, device_info in config_toml.items():
        if device_info.get('device_name') in connected_devices:
            config_temp += 'Device: ' + device + '\n'
            for key, value in device_info.items():
                config_temp += key + ': ' + str(value) + '\n'
            config_temp += '\n'    
    return config_temp




def save_data(experiment_name, data_path, experiment_start , experiment_completed, experimental_data, config):
    '''
    Sets up the data to be logged regarding the experiment, 'out' is the string to append to (with \n for a new line) 
    that will be written. Can add more things as we find the need. 

    Example: 
    --------
        >>> out += 'some data to add\n

    The save portion will try save to the specified directory, if it cant - it will attempt to dump it into the current working directory    
    '''
    experiment_name = experiment_name +'.spectre'
    experiment_name = name_checker((data_path + '/' + experiment_name))
    out = 'Experiment Name: '+ experiment_name + '\n'
    out +='Date Start: '+ experiment_start + '\n'
    out +='Date Completed: '+ experiment_completed + '\n'
    out += '\n\n'
    out += '%============================================%\nExperimental Configuration\n%============================================%\n\n\n'
    out += config + '\n'
    out += '%============================================%\nExperimental Data\n%============================================%\n\n\n'
    #to_save_data = data_prep(data)
    out += experimental_data + '\n'

    try:
        tfile = open(data_path  + '/' + experiment_name, 'a')
        tfile.write(out)
        tfile.close()
    except IOError as e:
        print('Directory doesnt exist!!')
        print('Saving to current working directory instead')
        pass
        try:
            data_path = os.path.abspath(os.getcwd())
            experiment_name = name_checker(data_path   + '/' + experiment_name)
            tfile = open(data_path  + '/' + experiment_name, 'a')
            tfile.write(out)
            tfile.close()
        except IOError as e:
            print(e) 
            print('Files failed to save')
            pass

def data_prep(experimental_data):
    data = pd.DataFrame.from_dict(experimental_data)
    data = data.to_string()
    return data