import serial
import time
import settings
from utils import threaded
import queue


class MasterModule:
    def __init__(self):
        self.port = False
        self.queue_tx = queue.Queue()
        self.queue_rx = queue.Queue()
        self.is_open = [True] * settings.NUMBER_OF_PRESSES
        self.is_opening = False
        self.readed_status = ''
        self.state_ask_counter = 100
        self.state = ''
        self.init_connection()
        self.main_handling()

    def serial_clear(self):
        if (self.MasterModule.inWaiting() > 0):
            try:
                self.MasterModule.read(self.MasterModule.inWaiting())
                time.sleep(0.05)
            except:
                pass
            self.MasterModule.flush()

    def init_connection(self):
        _ports_usb = ['/dev/ttyUSB{}'.format(number) for number in range(0, 20)]
        _ports_acm = ['/dev/ttyACM{}'.format(number) for number in range(0, 20)]
        _ports = _ports_usb + _ports_acm
        for port in _ports:
            try:
                self.MasterModule = serial.Serial(port, 
                                                  115200,
                                                  dsrdtr=True,
                                                  rtscts=True)
                if self.MasterModule.isOpen():
                    self.MasterModule.close()
                self.MasterModule = serial.Serial(port, 
                                                  115200,
                                                  dsrdtr=True,
                                                  rtscts=True)
                self.port = True
                time.sleep(0.5)
                self.serial_clear()
                time.sleep(0.5)
                break
            except serial.SerialException:
                pass

    def __del__(self):
        if self.port:
            self.MasterModule.close()

    def serial_write(self, data_to_send):
        self.MasterModule.write(str(data_to_send).encode('utf-8'))
        time.sleep(0.05)
        self.MasterModule.flush()

    def serial_read(self):
        try:
            return self.MasterModule.read(self.MasterModule.inWaiting()).decode(
                encoding='UTF-8', errors='ignore').rstrip()
        except:
            return None

    def read_queue_tx(self):
        try:
            command = self.queue_tx.get(block=False)
        except (queue.Empty,):
            command = None

        return command

    def read_queue_rx(self):
        try:
            command = self.queue_rx.get(block=False)
        except (queue.Empty,):
            command = None

        return command  

    def handle_queue_rx(self, command, sleep_time):
        while self.read_queue_rx() != command:
            self.queue_tx.put(command)
            time.sleep(sleep_time)

    def get_presses_states(self):
        self.serial_clear()
        self.serial_write('AE')
        
        self.readed_status = self.serial_read() or ''

    def handle_commands(self):
        command = self.read_queue_tx()
        if command:
            self.serial_write(command)
            rx_data = self.serial_read()
            if rx_data:
                self.queue_rx.put(rx_data)

    @threaded
    def main_handling(self):
        while self.port:
            self.get_presses_states()

            self.handle_commands()

            if self.state_ask_counter > 100:
                self.state_ask_counter = 0
                self.serial_write('ST')
                self.state = self.serial_read() or ''
            else:
                self.state_ask_counter += 1

            time.sleep(0.1)

    @threaded
    def open_press(self, press_id):
        press_label = str(press_id + 1).zfill(2)

        while self.is_opening:
            # wait to finish opening another press
            pass

        self.is_open[press_id] = False

        while not self.is_open[press_id]:
            if not self.is_opening:
                self.is_opening = True

                self.handle_queue_rx('Z02', 1)
                self.handle_queue_rx('R{}'.format(press_label), 30)
                self.handle_queue_rx('A{}'.format(press_label), 15)
                self.handle_queue_rx('B02', 6)
                self.handle_queue_rx('Z01', 1)

                self.is_opening = False
                self.is_open[press_id] = True

    def get_status_string(self):

        return self.readed_status

    def get_state_string(self):

        return self.state
