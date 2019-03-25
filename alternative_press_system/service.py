from api import ApiService
import settings


class AppService:
	def __init__(self, my_app):
		self.api = ApiService()
		self.my_app = my_app
		self.press_times = []
		self.init_values()
		print(self.press_times)

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
