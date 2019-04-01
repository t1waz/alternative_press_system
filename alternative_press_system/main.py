import os
os.environ['KIVY_GL_BACKEND'] = 'gl' # DUE TO RUNNING ON RASPI
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from service import AppService
from control import MasterModule
from kivy.properties import StringProperty
import threading


Builder.load_file('graphic.kv')


class MasterModuleThread(threading.Thread):
    def __init__(self, my_app):
        threading.Thread.__init__(self)
        self.master_module = MasterModule()
        self.app_service = AppService(my_app)

    def run(self):
        while True:
            readed_data = self.master_module.handle_control()
            #'S0A0Z1000B0Y0C0X0D0W0E0V0F0U0L'
            print(readed_data)
            self.app_service.main_handling(readed_data)


class MainWindow(Screen):
    system_status = StringProperty('')
    for index in range(1,7):
        mold = 'press_{}_mold_label'.format(index)
        state = 'press_{}_state_label'.format(index)
        time = 'press_{}_time_label'.format(index)
        exec(mold + '  = StringProperty()')
        exec(state + '  = StringProperty()')
        exec(time + '  = StringProperty()')

    def __init__(self, **kwargs):
        super(MainWindow,self).__init__(**kwargs)


class PressApp(App):
    def __init__(self, **kwargs):
        super(PressApp, self).__init__(**kwargs)

    def build(self):
        main_window = MainWindow()
        MasterModuleThread(main_window).start()
        return main_window


if __name__ == '__main__':
    PressApp().run()
