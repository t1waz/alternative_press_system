from api import ApiService
import settings


class AppService:
    def __init__(self, my_app):
        self.api = ApiService()
        self.my_app = my_app
        self.press_times = []
        self.switchgear_status = ''
        self.presses_statuses = [''] * settings.NUMBER_OF_PRESSES
        self.presses_times = [0] * settings.NUMBER_OF_PRESSES
        self.readed_data = ''
        self.init_values()

    def return_time_format(self, seconds):
        hours = int(seconds/3600)
        minutes = int((seconds - hours*3600)/60)
        seconds = seconds - hours*3600 - minutes*60

        return '{}:{}:{}'.format(str(hours).zfill(2),
                                 str(minutes).zfill(2),
                                 str(seconds).zfill(2))

    def init_values(self):
        presses = self.api.get_endpoint_data('presses')
        for index, press in enumerate(presses):
            pressing_time = self.return_time_format(press['press_time'])
            setattr(self.my_app, 'press_{}_mold_label'.format(index+1), press['mold'])
            setattr(self.my_app, 'press_{}_time_label'.format(index + 1), pressing_time)
            setattr(self.my_app, 'press_{}_state_label'.format(index + 1), 'READY')
            self.press_times.append(press['press_time'])

    def states_from_control_string(self, control_string):
        presses_statuses_index = [0]*settings.NUMBER_OF_PRESSES
        switchgear_status = 0

        if control_string.startswith('S'):
            switchgear_status = int(control_string[1])
            for index, info in enumerate(settings.PRESSES_INFO):
                presses_statuses_index[index] = int(self.string_between_chars(string=control_string,
                                                                        start=info[0],
                                                                        end=info[1]))
                presses_times[index] = int(self.string_between_chars(string=control_string,
                                                                     start=info[1],
                                                                     end=info[2]))

        return settings.SWITCHGEAR_STATE[switchgear_status], \
               [settings.PRESS_STATE[index] for index in presses_statuses_index], \
               presses_times, \
               readed_data

    def label_handling(self, control_string):
        self.return_states_from_control_string(control_string)