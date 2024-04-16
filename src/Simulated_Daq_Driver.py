import sys
import glob
import serial
import time
import random as rd



class Test_Daq:
    def __init__(self, config, emulate = True):
            '''
            a simulated device
            '''
            self.emulation = True
            self.name = 'simulated daq'
            if self.emulation == False:
                    print('This device is not real, it cannot be used in a non emulated environment')
                    print('Would you like to emulate the device instead?')
            else: 
                self.connect(config)
                self.instrument =  print("Simulated Daq Sucsessfully emulated")
                self.name = 'simulated daq'
            return
    
    def connect(self, config):
        self.name = 'simulated daq'
    # Find the short name associated with the full device name
        for device, device_config in config.items():
            if device_config.get('device_name') == self.name:
                break
        else:
            raise ValueError(f"Device {self.name} not found in configuration file")

        print(device_config)

    # Set the integration time from the device configuration
        self.integration_time = device_config.get('integration_time')


    def measure(self) -> float:
        return  rd.uniform(0.0, 10) * self.integration_time     

                 

          


