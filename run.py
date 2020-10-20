from obscontroller import ObsController
from rocksniffer import Rocksniffer
from iniReader import INIReader
from time import sleep
from logger import log

conf = INIReader("config.ini")

client = ObsController(
    conf.get_value("OBSWebSocket", "host"),
    conf.get_value("OBSWebSocket", "port"),
    conf.get_value("OBSWebSocket", "pass")
)
sniffer = Rocksniffer(
    conf.get_value("RockSniffer", "host"),
    conf.get_value("RockSniffer", "port"),
)

error_wait_time = 1

def error(message):
    global error_wait_time
    error_wait_time = min(error_wait_time * 2, 60)
    log.warning(message)
    log.warning("Re-trying in {} seconds".format(error_wait_time))
    sleep(error_wait_time)

# Main loop
while True:
    sleep(0.1)
    conf.reload()
    # Updating configuration
    current_configuration = [client.IP, client.PORT, client.PASS]
    client.IP = conf.get_value("OBSWebSocket", "host")
    client.PORT = conf.get_value("OBSWebSocket", "port")
    client.PASS = conf.get_value("OBSWebSocket", "pass")
    client.cooldown = conf.get_value("Behaviour", "cooldown", int)
    client.forbidden = conf.get_value("Behaviour", "forbidden_switch_on_scenes", list)
    new_configuration = [client.IP, client.PORT, client.PASS]

    if current_configuration != new_configuration:
        log.notice("New configuration for OBSWebSocket. Restarting client..")
        client.socket = None

    sniffer.host = conf.get_value("RockSniffer", "host")
    sniffer.port = conf.get_value("RockSniffer", "port")
    # Connecting to OBS controller
    try:
        alive = client.socket
        if not alive:
            log.notice("Connecting to OBS WebSocket..")
        client.keep_alive()
        if not alive:
            log.notice("Connected.")
        error_wait_time = 1
    # Waiting longer and longer if failed.
    except ConnectionError:
        error("Failed to connect to OBS WebSocket. Please check your config.")
        continue

    # Updating Rocksniffer
    try:
        if not sniffer.memory:
            log.notice("Starting sniffing..")
        sniffer.update()
    except ConnectionError:
        log.notice("Rocksniffer update failed.")

    if not sniffer.success:
        continue

    # Behaviour
    try:
        # Case in game
        if sniffer.in_game and not sniffer.in_pause:
            client.smart_switch(conf.get_value('Behaviour', "in_game"))
        # Case in Pause
        elif sniffer.in_game and sniffer.in_pause:
            client.smart_switch(conf.get_value('Behaviour', "paused"))
        # Case in menu
        elif not sniffer.in_game:
            client.smart_switch(conf.get_value('Behaviour', "in_menu"))
    except:
        log.warning("Error using OBS WebSocket.")
        client.socket = None
