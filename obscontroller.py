from obswebsocket import obsws, requests
import time
import logger

class ObsController:
    def __init__(self, IP, PORT, PASS=None, cooldown=3, forbidden=[]):
        self.socket = None
        self.IP = IP
        self.PORT = PORT
        self.PASS = PASS

        self.last_scene = None
        self.last_switch = 0
        self.cooldown = cooldown
        self.forbidden = forbidden



    def socket_init(self):
        try:
            self.socket = obsws(self.IP, self.PORT, None if self.PASS == "" else self.PASS)
            self.socket.connect()
        except:
            self.socket = None
            raise ConnectionError



    def keep_alive(self):
        if self.socket is None:
            self.socket_init()


    @property
    def current_scene(self):
        return self.socket.call(requests.GetCurrentScene()).datain['name']


    def go_to_scene(self, scene):
        self.socket.call(requests.SetCurrentScene(scene))
        self.last_scene = scene
        self.last_switch = time.time()

    def smart_switch(self, scene):
        if self.last_switch + self.cooldown > time.time():
            return

        current_scene = self.current_scene
        if current_scene in self.forbidden:
            return

        if scene != self.last_scene:
            logger.log.log("Switching to [{}]".format(scene))
            self.go_to_scene(scene)
