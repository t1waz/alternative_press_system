from api import ApiService
import settings


class AppService:
	def __init__(self, my_app):
		self.api = ApiService()
		self.my_app = my_app
		self.init_values()

	def init_values(self):
		presses = self.api.get_endpoint_data('presses')
		for press in presses:
			pass