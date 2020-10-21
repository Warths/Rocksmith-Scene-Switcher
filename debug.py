import time
from logger import log

class Debugger:
    def __init__(self, debug, interval):
        self.debug = debug
        self.interval = interval

        self.last_log = 0

    def log(self, message):
        if self.debug:
            log.discrete("[DEBUG] " + message)

    def log_on_interval(self, message):
        if self.last_log + self.interval < time.time():
            self.log(message)
            self.last_log = time.time()
