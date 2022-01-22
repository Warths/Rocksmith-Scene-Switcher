import time

from obswebsocket import obsws, requests

import logger


class ObsController:
    def __init__(self, IP, PORT, PASS=None, cooldown=3, forbidden=[]):
        """

        :param IP: OBS Websocket Host (should be localhost)
        :param PORT: OBS Websocket Port (default = 4444)
        :param PASS: Password. Strongly recommended
        :param cooldown: minimum time between two scene change
        :param forbidden: list of the scenes that doesn't allows for switching
        """
        self.socket = None
        self.IP = IP
        self.PORT = PORT
        self.PASS = PASS

        # Behaviour related variables
        self.last_scene = None
        self.last_switch = 0
        self.cooldown = cooldown
        self.forbidden = forbidden

    def socket_init(self):
        """
        Init the socket. Raise ConnectionError if failed.
        :return:
        """
        try:
            self.socket = obsws(self.IP, self.PORT, None if self.PASS == "" else self.PASS)
            self.socket.connect()
        except:
            self.socket = None
            raise ConnectionError

    def keep_alive(self):
        """
        Init the socket if dead, otherwise do nothing
        """
        if self.socket is None:
            self.socket_init()

    @property
    def current_scene(self):
        """
        Get the current Scene.
        :return: Str. Scene name
        """
        return self.socket.call(requests.GetCurrentScene()).datain['name']

    def go_to_scene(self, scene):
        """
        Switch to a scene. Allows for non-existing scenes
        :param scene: Scene name
        """
        self.socket.call(requests.SetCurrentScene(scene))
        self.last_scene = scene
        self.last_switch = time.time()

    def smart_switch(self, scene):
        # Skipping if cooldown not reached
        if self.last_switch + self.cooldown > time.time():
            return

        # Skipping if current scene forbids auto change
        current_scene = self.current_scene
        if current_scene in self.forbidden:
            return

        # Only switching if the last targeted scene is different
        if scene != self.last_scene:
            logger.log.log("Switching to [{}]".format(scene))
            self.go_to_scene(scene)
