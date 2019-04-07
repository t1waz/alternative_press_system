from api import ApiService
from control import MasterModule
import settings
from utils import string_between_chars, get_time_format
from copy import deepcopy


class AppService:
    nextid = 0
    def __init__(self, my_app):
        self.api = ApiService()
        self.master_module = MasterModule()
        self.my_app = my_app
        self.press_time = [0] * settings.NUMBER_OF_PRESSES
        self.current_time = [0] * settings.NUMBER_OF_PRESSES
        self.is_opening = False
        self.init_values()

    def set_label(self, label, value):
        setattr(self.my_app, label, value)

    def init_values(self):
        presses = self.api.get_endpoint_data('presses')
        self.set_label('system_status', 'STARTING')
        for index, press in enumerate(presses):
            self.press_time[index] = deepcopy(int(press['press_time']))
            self.current_time[index] = deepcopy(int(press['press_time']))
            time = get_time_format(self.press_time[index])

            self.set_label('press_{}_mold_label'.format(index+1), press['mold'])
            self.set_label('press_{}_time_label'.format(index + 1), time)
            self.set_label('press_{}_state_label'.format(index + 1), 'READY')

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
            self.current_time[index] = max(self.press_time[index] - time_already_pressed,0)
            current_time = get_time_format(self.current_time[index])
            current_state = settings.PRESS_STATE.get(string_between_chars(s=control_string,
                                                                          start=info[0],
                                                                          end=info[1]), 'ERROR')
            self.set_label('press_{}_state_label'.format(index + 1), current_state)
            self.set_label('press_{}_time_label'.format(index + 1), current_time)

    def main_handling(self):
        readed_string = self.master_module.get_status_string()
        presses_is_open = self.master_module.get_presses_open_state()

        self.handle_labels_from_control_string(readed_string)
        print(readed_string)
        for inex, remaining_time in enumerate(self.current_time):
            if remaining_time == 0:
                if presses_is_open[index] == True:
                    self.master_module.open_press(index)



