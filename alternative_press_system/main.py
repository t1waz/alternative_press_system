import os
os.environ['KIVY_GL_BACKEND'] = 'gl' # DUE TO RUNNING ON RASPI
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from service import AppService
from control import MasterModule
import threading


Builder.load_file('graphic.kv')


class MasterModuleThread(threading.Thread):
    def __init__(self, my_app):
        threading.Thread.__init__(self)
        self.master_module = MasterModule()
        self.app_service = AppService(my_app)

    def run(self):
        while True:
        	pass


class MainWindow(Screen):

    def __init__(self, **kwargs):
        super(MainWindow,self).__init__(**kwargs)


class PressApp(App):
	def __init__(self, **kwargs):
        super(ScanApp, self).__init__(**kwargs)

    def build(self):
    	main_window = MainWindow()
    	MasterModuleThread(main_window).start()
        return main_window


if __name__ == '__main__':
    PressApp().run()
