import sys
import glob
import serial
import serial.tools.list_ports
import time

class HR640_Spectrometer:
    def __init__(self, emulate = False):
            self.emulation = emulate
            if self.emulation == False:
                if sys.platform.startswith('win'):
                    ports = ['COM%s' % (i + 1) for i in range(256)]  
                elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                    # this excludes your current terminal "/dev/tty"
                    ports = glob.glob('/dev/tty[A-Za-z]*')
                elif sys.platform.startswith('darwin'):
                    ports = glob.glob('/dev/tty.*')
                else:
                    raise EnvironmentError('Unsupported platform')

                result = []

                # Find spectrometer using serial.tools
                ports_full = list( serial.tools.list_ports.comports() )
            
                for port in ports_full:
                    if (port.description.startswith("usb serial converter")):
                        port.interface
                        if (port.manufacturer.startswith("ftdi")):
                            print("Found potential HR640")
                            result.append(port.device)
                self.ser_ports = result
                self.connect()

                self.name = 'HR640'
                if self.instrument == 'not found':
                    print('HR640 spectrometer not found, try reconecting. If issues persist, restart python')
                    print('Would you like to emulate the device instead?')
            else: 
                self.instrument =  print("HR640 spectrometer Sucsessfully emulated")
                self.wavelength = "600"
            return


    def connect(self):
            if not self.ser_ports:
                print("No devices connected, or device is already connected")
            else:  
                print(self.ser_ports)  
                for port in self.ser_ports:
                    try:
                        self.instrument = serial.Serial(port)              
                        self.instrument.write(b'G\r')
                        self.wavelength = self.instrument.read(8)
                        print(self.wavelength) 
                    except:
                        print('Spectrometer device not found, try reconnecting') 

    def get_wavelength(self,grating_factor = 1.5, calibration_factor = 27):
        if self.emulation == True:
            return self.wavelength
        else:
            self.instrument.flushInput()
            self.instrument.flushOutput()  
            self.instrument.write(b'G\r')
            wavelength= self.instrument.read(8).decode('utf-8').strip('a\r') 
            print(wavelength)
            wavelength = (float(wavelength) / grating_factor) + calibration_factor #Does conversion of settings
            self.wavelength= '{0:.2f}'.format(wavelength) #Returns a str with 2 dp of the real wavelength
            time.sleep(0.05)
        return(self.wavelength)   
    
    def goto_wavelength(self, wavlen, grating_factor = 1.5, calibration_factor = 27):
        if self.emulation == True:
            self.wavelength = (str(wavlen))
        else:    

            self.instrument.flushInput()
            self.instrument.flushOutput()  
            wavlen_spec = (float(wavlen) - calibration_factor) * grating_factor  
  
            wavlen_spec = f'C{wavlen_spec:.2f}\r'.encode()
            print(wavlen_spec)  #Changes from 'real' wavelength to required spectrometer settings
            self.instrument.write(wavlen_spec)
            self.instrument.read(8)