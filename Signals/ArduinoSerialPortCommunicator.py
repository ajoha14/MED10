import serial


class SerialReader:
    def __init__(self):
        self.ser = serial.Serial(port='COM4', baudrate=9600)
        if not self.ser.is_open:
            self.ser.open()

    def current_input(self):
        return self.ser.readline()

