import numpy as np
import random as rd
import scipy.stats as stats
import matplotlib.pyplot as plt

def Gamma2sigma(Gamma):
    '''Function to convert FWHM (Gamma) to standard deviation (sigma)'''
    return Gamma * np.sqrt(2) / ( np.sqrt(2 * np.log(2)) * 2 )

def random_spectra(X):

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

