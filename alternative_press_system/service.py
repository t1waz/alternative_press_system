from api import ApiService
import settings
from utils import string_between_chars, return_time_format

class AppService:
    def __init__(self, my_app):
        self.api = ApiService()
        self.my_app = my_app
        self.init_values()

    def set_label(label, value):
        setattr(self.my_app, label, value)

    def init_values(self):
        presses = self.api.get_endpoint_data('presses')
        self.my_app.system_status = 'STARTING'
        for index, press in enumerate(presses):
            pressing_time = return_time_format(press['press_time'])
            self.set_label('press_{}_mold_label'.format(index+1), press['mold'])
            self.set_label('press_{}_time_label'.format(index + 1), pressing_time)
            self.set_label('press_{}_state_label'.format(index + 1), 'READY')

    def return_states_from_control_string(self, control_string):
        if control_string.startswith('S'):
            print('aa')
            self.my_app.system_status = settings.SWITCHGEAR_STATE[int(control_string[1])]
            for index, info in enumerate(settings.PRESSES_INFO):
                status = int(string_between_chars(string=control_string,
                                                  start=info[0],
                                                  end=info[1]))
                self.set_label('press_{}_state_label'.format(index + 1), settings.PRESS_STATE[press_status])

                # self.presses_times = int(string_between_chars(string=control_string,
                #                                               start=info[1],
                #                                               end=info[2]))

    def label_handling(self, control_string):
        self.return_states_from_control_string(control_string)