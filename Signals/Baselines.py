from misc.buffer import Buffer
from Signals import hrProc
from Signals.ArduinoSerialPortCommunicator import SerialReader

class baseline:
    def __init__(self, port, hz=100, duration=60):
        self.hz = hz
        self.duration = duration
        #buffers
        self.timestamps = Buffer(hz*duration)
        self.baseHR = Buffer(hz*duration)
        self.baseGSR = Buffer(hz*duration)
        #Serial Settings
        self.serial = SerialReader(port='COM5')
    
    def gatherBaseline(self):
        if self.serial.ser is not None:
            isGathering = True
            print('Gathering Baseline physiological signals')
            while isGathering:
                currentData = self.serial.current_data()
                if currentData is not 'error' and not self.timestamps.isfull():
                    time, gsr, hr = currentData.split(',', 3)
                    self.baseHR.add(float(hr))
                    self.baseGSR.add(float(gsr))
                    self.timestamps.add(time)
        else:
            print("Unable to contact arduino, Baseline could not be calculated")






    

        

