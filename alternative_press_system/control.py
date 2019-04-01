import serial
import time
import settings


class MasterModule:
    def __init__(self):
        self.switchgear_status = 0
        self.init_connection()

    def init_connection(self):
        _ports_usb = ['/dev/ttyUSB{}'.format(number) for number in range(0, 20)]
        _ports_acm = ['/dev/ttyACM{}'.format(number) for number in range(0, 20)]
        _ports = _ports_usb + _ports_acm
        self.port = False
        for port in _ports:
            try:
                self.MasterModule = serial.Serial(port, 
                                                  115200,
                                                  dsrdtr=True,
                                                  rtscts=True)
                if self.MasterModule.isOpen():
                    self.MasterModule.close()
                    print(port)
                self.MasterModule = serial.Serial(port, 
                                                  115200,
                                                  dsrdtr=True,
                                                  rtscts=True)
                self.port = True
                print("port ", port)
                time.sleep(1)
                if (self.MasterModule.inWaiting() > 0):
                    self.MasterModule.read(MasterModule.inWaiting())
                    self.MasterModule.flush()
                time.sleep(1)
                break
            except serial.SerialException:
                pass

    def __del__(self):
        if self.port:
            self.MasterModule.close()

    def serial_write(self, data_to_send):
        self.MasterModule.write(str(data_to_send).encode('utf-8'))
        self.MasterModule.flush()

    def serial_clear(self):
        if (self.MasterModule.inWaiting() > 0):
            try:
                self.MasterModule.read(self.MasterModule.inWaiting())
                time.sleep(0.05)
            except:
                pass
            self.MasterModule.flush()

    def serial_read(self):
        return self.MasterModule.read(self.MasterModule.inWaiting()).decode(
                encoding='UTF-8', errors='ignore').rstrip()

    def ask_data(self):
        self.serial_clear()
        self.serial_write('AE')
        time.sleep(0.5)
        readed_data = self.serial_read()

        return readed_data

    def open_press(self, press_id):
        if str(press_id) < 2:
            press_label = '0{}'.format(press_id)
        else:
            press_label = str(press_id)

        self.serial_write('Z02')
        time.sleep(1)
        self.serial.clear()
        self.serial_write('R{}'.format(press_label))
        time.sleep(30)
        self.serial_clear()
        self.serial_write('A{}'.format(press_label))
        time.sleep(6)
        self.serial_clear()
        self.serial_write('B{}'.format(press_label))
        time.sleep(6)
        self.serial_clear()
        self.serial_write('Z01')

    def handle_control(self):
        if self.port:
            return self.ask_data()
        else:
            return ''
