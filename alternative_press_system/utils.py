import threading
'''
    Utils functions and shit
'''


def string_between_chars(s, start, end):
    try:
        return s[s.index(start)+1: s.index(end)]
    except (IndexError,):
        return ''

def get_time_format(seconds):
    try:
        hours = int(seconds/3600)
        minutes = int((seconds - hours*3600)/60)
        seconds = seconds - hours*3600 - minutes*60

        return '{}:{}:{}'.format(str(hours).zfill(2),
                                 str(minutes).zfill(2),
                                 str(seconds).zfill(2))
    except:
        return '00:00:00'

def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper
