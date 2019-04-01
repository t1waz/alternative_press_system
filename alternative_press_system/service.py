from api import ApiService
import settings
from utils import string_between_chars, get_time_format, threaded
import time


class AppService:
    def __init__(self, my_app):
        self.api = ApiService()
        self.my_app = my_app
        self.is_opening = False
        self.press_time = [0] * settings.NUMBER_OF_PRESSES
        self.init_values()

    def set_label(self, label, value):
        setattr(self.my_app, label, value)

    def init_values(self):
        presses = self.api.get_endpoint_data('presses')
        self.set_label('system_status', 'STARTING')
        for index, press in enumerate(presses):
            self.press_time[index] = int(press['press_time'])
            time = get_time_format(self.press_time[index])

            self.set_label('press_{}_mold_label'.format(index+1), press['mold'])
            self.set_label('press_{}_time_label'.format(index + 1), time)
            self.set_label('press_{}_state_label'.format(index + 1), 'READY')

    @threaded
    def open_press(self, press_id):
        started = True
        while started:
            if self.is_opening == False:
                self.is_opening = True
                # DO SHIT
                self.is_opening = False
                started = False

    def handle_labels_from_control_string(self, control_string):
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
            current_time = get_time_format(self.press_time[index] - time_already_pressed)
            current_state = settings.PRESS_STATE.get(string_between_chars(s=control_string,
                                                                          start=info[0],
                                                                          end=info[1]), 'ERROR')
            self.set_label('press_{}_state_label'.format(index + 1), current_state)
            self.set_label('press_{}_time_label'.format(index + 1), current_time)

    def main_handling(self, control_string):
        self.handle_labels_from_control_string(control_string)


