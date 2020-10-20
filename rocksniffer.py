import requests

class Rocksniffer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.memory = None
        self.samples = [0, 0, 0]


    def update(self):
        try:
            self.memory = requests.get("http://{}:{}/".format(self.host, self.port)).json()
            if self.memory["success"]:
                self.samples.append(self.memory['memoryReadout']['songTimer'])
                if len(self.samples) > 3:
                    self.samples.pop(0)
        except:
            raise ConnectionError

    @property
    def success(self):
        try:
            return self.memory['success']
        except:
            return False


    @property
    def in_pause(self):
        return not self.samples[0] < self.samples[1] < self.samples[2]

    @property
    def currentState(self):
        return self.memory["currentState"]

    @property
    def in_game(self):
        return self.currentState in range(3, 5)