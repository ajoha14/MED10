import serial
from datetime import datetime

class SerialReader:
    def __init__(self, port):
        self.port = port
        try:
            self.ser = serial.Serial(port=port, baudrate=9600)
        except serial.SerialException as e:
            print(e)
            self.ser = None
        if self.ser is not None and not self.ser.is_open:
            self.ser.open()

    def current_data(self):
        #[:-2] removes one of the 'newline' at the end of all inputs
        output = datetime.utcnow().strftime('%m_%d-%H_%M_%S.%f') + "," + self.ser.readline().decode("utf-8")[:-2]
        #output = inputSerial.split(',', 2)
        if output.count(",") is not 2:
            return "error"
        return output


