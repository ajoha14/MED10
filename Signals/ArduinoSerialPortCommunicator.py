import serial


class SerialReader:
    def __init__(self, port):
        self.ser = serial.Serial(port=port, baudrate=9600)
        if not self.ser.is_open:
            self.ser.open()

    def current_data(self):
        #[:-2] removes one of the 'newline' at the end of all inputs
        output = self.ser.readline().decode("utf-8")[:-2]
        print(output)
        if output.count(",") is not 1:
            return "error"
        return self.ser.readline().decode("utf-8")[:-2]

