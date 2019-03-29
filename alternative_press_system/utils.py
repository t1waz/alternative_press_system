'''
	Utils functions and shit
'''

def string_between_chars(string, start, end):
	return string[string.index(start)+1: string.index(end)]

def return_time_format(seconds):
	hours = int(seconds/3600)
	minutes = int((seconds - hours*3600)/60)
	seconds = seconds - hours*3600 - minutes*60

	return '{}:{}:{}'.format(str(hours).zfill(2),
                           	 str(minutes).zfill(2),
                             str(seconds).zfill(2))