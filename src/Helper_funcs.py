import numpy as np
import random as rd
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
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

def name_checker(self,fname_path):
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


def save_data(experiment_name, data_path, experiment_start ,experiment_completed):
    '''
    Sets up the data to be logged regarding the experiment, 'out' is the string to append to (with \n for a new line) 
    that will be written. Can add more things as we find the need. 

    Example: 
    --------
        >>> out += 'some data to add\n

    The save portion will try save to the specified directory, if it cant - it will attempt to dump it into the current working directory    
    '''
    experiment_name = experiment_name +'.txt'
    experiment_name = name_checker(data_path + experiment_name)
    out = 'Experiment Name: '+ experiment_name + '\n'
    out +='Date Start: '+ experiment_start + '\n'
    out +='Date Completed: '+ experiment_completed + '\n'
    out += '\n\n'
    out += '%============================================%\nExperimental Configuration\n%============================================%\n\n\n'
    #out += config
    out += '%============================================%\nExperimental Data\n%============================================%\n\n\n'
    #to_save_data = data_prep(data)
    try:
        tfile = open(data_path + experiment_name, 'a')
        tfile.write(out)
        tfile.close()
    except IOError as e:
        print('Directory doesnt exist!!')
        print('Saving to current working directory instead')
        pass
        try:
            data_path = os.path.abspath(os.getcwd()) + '\\'
            experiment_name = name_checker(data_path + experiment_name)
            tfile = open(data_path + experiment_name, 'a')
            tfile.write(out)
            tfile.close()
        except IOError as e:
            print(e) 
            print('Files failed to save')
            pass