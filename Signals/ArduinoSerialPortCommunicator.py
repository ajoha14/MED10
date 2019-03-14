import serial


class SerialReader:
    def __init__(self, port):
        self.ser = serial.Serial(port=port, baudrate=9600)
        if not self.ser.is_open:
            self.ser.open()

    def current_input(self):
        return self.ser.readline()

