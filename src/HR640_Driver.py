#this implemnetation needs to be checked.

import pyvisa
#this is subject to change depending on USB hub, this needs to be changed to a handshake
class HR640_Spectrometer:
    def __init__(self, emulate = False):
            self.emulation = emulate
            if self.emulation == False:
                self.rm = pyvisa.ResourceManager()
                self.resource_adress = 'not found'
                resources = rm.list_resources()
                for i in range(len(resources)):
                    my_instrument = rm.open_resource(resources[i])
                    query = my_instrument.query('*IDN?').strip()
                    
                    if query == 'SPECTROMETER': ## Needs to be changed to its actual value
                        self.resource_adress = resources[i]
                        self.instrument = my_instrument
                        self.instrument.read_termination = '\r'
                        print('HR640 spectrometer successfully connected')
                if self.resource_adress == 'not found':
                    print('HR640 spectrometer not found, try reconecting. If issues persist, restart python')
                    print('Would you like to emulate the device instead?')
            else: 
                 self.instrument =  print("HR640 spectrometer Sucsessfully emulated")
                 self.wavelength = "600"
            return
    
    def get_wavelength(self,grating_factor = 1.5, calibration_factor = 27):
        if self.emulation == True:
            return self.wavelength
        else:
            wavelength= self.instrument.query("G")[1:] #Cuts of the 1st "C" character
            wavelength = (float(a) / grating_factor) + calibration_factor #Does conversion of settings
            self.wavelength= '{0:.2f}'.format(wavelength) #Returns a str with 2 dp of the real wavelength
        return(self.wavelength)    

    def goto_wavelength(self, wavlen, grating_factor = 1.5, calibration_factor = 27):
        if self.emulation == True:
           self.wavelength = (str(wavlen))
        else:    
            wavlen_spec = (float(wavlen) - calibration_factor) * grating_factor  
            wavlen_spec = "C" + "{:.2f}".format(float(wavlen_spec))   #Changes from 'real' wavelength to required spectrometer settings
            self.instrument.write(wavlen_spec)


