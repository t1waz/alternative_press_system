from api import ApiService
from control import MasterModule
import settings
from utils import string_between_chars, get_time_format
from copy import deepcopy


class AppService:
    def __init__(self, my_app):
        self.api = ApiService()
        self.master_module = MasterModule()
        self.my_app = my_app
        self.press_time = [0] * settings.NUMBER_OF_PRESSES
        self.current_time = [0] * settings.NUMBER_OF_PRESSES
        self.is_open_started = [False] * settings.NUMBER_OF_PRESSES
        self.init_values()

    def set_label(self, label, value):
        setattr(self.my_app, label, value)

    def init_state_message_window(self):
        state_string = self.master_module.get_state_string()
        active_input_modules = string_between_chars(s=state_string,
                                                    start='I',
                                                    end='R')
        active_relay_modules = string_between_chars(s=state_string,
                                                    start='R',
                                                    end='L')

        try:
            input_string = str(bin(int(active_input_modules))[2:]).zfill(settings.NUMBER_OF_PRESSES)[::-1]
            relay_string = str(bin(int(active_relay_modules))[2:]).zfill(settings.NUMBER_OF_PRESSES)[::-1]
        except:
            input_string = ''
            relay_string = ''

        input_modules_status = ['ACTIVE' if status == '1' else 'DISABLE' for status in list(input_string)]
        relay_modules_status = ['ACTIVE' if status == '1' else 'DISABLE' for status in list(relay_string)]

        for index, status in enumerate(input_modules_status):
            self.my_app.message_labels_input_modules.append('INP {}      {}'.format(index + 1, status))
        
        for index, status in enumerate(relay_modules_status):
            self.my_app.message_labels_relay_modules.append('REL {}      {}'.format(index + 1, status))

    def init_times_and_molds(self):
        presses = self.api.get_endpoint_data('presses')
        self.set_label('system_status', 'STARTING')
        for index, press in enumerate(presses):
            self.press_time[index] = deepcopy(int(press['press_time']))
            self.current_time[index] = deepcopy(int(press['press_time']))
            time = get_time_format(self.press_time[index])

            self.set_label('press_{}_mold_label'.format(index + 1), press['mold'])
            self.set_label('press_{}_time_label'.format(index + 1), time)
            self.set_label('press_{}_state_label'.format(index + 1), 'READY')    

    def init_values(self):
        self.init_times_and_molds()
        self.init_state_message_window()

    def handle_labels_from_control_string(self, control_string):
        if not control_string:
            return 

        if not control_string.startswith('S'):
            return 

        switchgear = settings.SWITCHGEAR_STATE.get(string_between_chars(s=control_string,
                                                                        start='S',
                                                                        end='A'), 'ERROR')
        self.set_label('system_status', switchgear)
        for index, info in enumerate(settings.PRESSES_INFO):
            time_already_pressed = int(string_between_chars(s=control_string,
                                                            start=info[1],
                                                            end=info[2]))
            self.current_time[index] = max(self.press_time[index] - time_already_pressed, 0)
            current_time = get_time_format(self.current_time[index])
            current_state = settings.PRESS_STATE.get(string_between_chars(s=control_string,
                                                                          start=info[0],
                                                                          end=info[1]), 'ERROR')
            self.set_label('press_{}_state_label'.format(index + 1), current_state)
            self.set_label('press_{}_time_label'.format(index + 1), current_time)

    def main_handling(self):
        readed_string = self.master_module.get_status_string()

        self.handle_labels_from_control_string(readed_string)

        for index, remaining_time in enumerate(self.current_time):
            if remaining_time == 0:
                if not self.is_open_started[index]:
                    self.master_module.open_press(index)
                    self.is_open_started[index] = True
            else:
                self.is_open_started[index] = False

