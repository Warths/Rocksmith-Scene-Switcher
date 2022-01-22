from time import sleep

from debug import Debugger
from iniReader import INIReader
from logger import log
from obscontroller import ObsController
from rocksniffer import Rocksniffer

# Initializing main objects
# Configuration
conf = None
try:
    conf = INIReader("config.ini")
except FileNotFoundError:
    log.notice('A config.ini file was created. Fill it, then relaunch RocksmithSceneSwitcher.')
    log.notice('Press any key to exit this program.')
    input()
    exit(0)

debug = Debugger(
    conf.get_value("Debugging", "debug", int),
    conf.get_value("Debugging", "log_state_interval", int)
)
# OBS Web Socket Client / OBS controller abstraction
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
    """
    log Error with incremental wait time.
    :param message: message to log as a warning
    """
    global error_wait_time
    error_wait_time = min(error_wait_time * 2, 60)
    log.warning(message)
    log.warning("Re-trying in {} seconds".format(error_wait_time))
    sleep(error_wait_time)


def get_debug_message():
    return "Game:{sniffer.in_game} " \
           "Pause:{sniffer.in_pause} " \
           "Tsamples:{sniffer.samples} " \
           "RsState:{sniffer.currentState} " \
           "LastScene:{client.last_scene}".format(sniffer=sniffer, client=client)


# Init debug
debug.log("Debugging starting.")
debug.log("[Behaviour]")
for k, v in conf.content["Behaviour"].items():
    debug.log("{} = {}".format(k, v))


def update_conf():
    # Updating OBS WebSocket configurations
    client_current_config = [client.IP, client.PORT, client.PASS]
    client.IP = conf.get_value("OBSWebSocket", "host")
    client.PORT = conf.get_value("OBSWebSocket", "port")
    client.PASS = conf.get_value("OBSWebSocket", "pass")
    client.cooldown = conf.get_value("Behaviour", "cooldown", int)
    client.forbidden = conf.get_value("Behaviour", "forbidden_switch_on_scenes", list)
    client_new_config = [client.IP, client.PORT, client.PASS]
    # Killing Socket if configuration has been changed
    if client_current_config != client_new_config:
        log.notice("New configuration for OBSWebSocket found! Restarting client..")
        client.socket = None
    # Updating Debug configurations
    debug.debug = conf.get_value("Debugging", "debug", int)
    debug.interval = conf.get_value("Debugging", "log_state_interval", int)
    # Updating Rocksniffer Configurations
    sniffer.host = conf.get_value("RockSniffer", "host")
    sniffer.port = conf.get_value("RockSniffer", "port")


# Main loop
while True:
    # Sleep a bit
    sleep(0.1)

    # Reload the config.
    reloaded = conf.reload()
    if reloaded:
        log.notice("Configuration reloaded (changed).")
        update_conf()

    # Connecting / Keeping OBS Controller alive
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

    # Updating Rocksniffer internal Values
    try:
        #
        if not sniffer.memory:
            log.notice("Starting sniffing..")
        sniffer.update()
    except ConnectionError:
        # Restarting the loop and cleaning memory if implicitly failed
        import traceback

        traceback.print_exc()
        sniffer.memory = None
        log.notice("Updating Rocksniffer internal Values failed!")
        continue

    # If sniff failed explicitly, restarting the loop
    if not sniffer.success:
        continue

    # Interval debugging
    debug.log_on_interval(get_debug_message())

    # Main Logic
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

    # Killing socket if any errors occurred
    except:
        log.warning("Error using OBS WebSocket.")
        client.socket = None
