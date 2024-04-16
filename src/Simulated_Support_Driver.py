class Test_Support:
    def __init__(self, config):
            '''
            a simulated device
            '''
            
            self.name = 'simulated support instrument'

            self.connect(config)
            self.instrument =  print("Simulated Support Instrument Sucsessfully emulated")
   
            return
    
    def connect(self, config):
    # Find the short name associated with the full device name
        for device, device_config in config.items():
            if device_config.get('device_name') == self.name:
                break
        else:
            raise ValueError(f"Device {self.name} not found in configuration file")

        print(device_config)

    # Set the integration time from the device configuration
        self.laser_temp = device_config.get('integration_time')
        self.laser_power = device_config.get('laser_power')
        self.time_on = device_config.get('time_on')
        self.time_off = device_config.get('time_off')
        self.time_scale = device_config.get('time_scale')