# Rocksmith Scene Switcher

Python program that uses Rocksniffer and OBS Web Socket to automatically switch your OBS Studio scene depending on Rocksmith state.

# Features!

  - Supports pausing the game and navigating through sections
  - Support blacklisting scene from switching (to lock Switcher's depending on the current scene)
  - Supports adding a customizable cooldown between changes
  - Support hot-changes on the config (optimized on latest version!).

# How to use ? 

Before using this software, you need to be sure about 2 things : 
- You have Rocksniffer running with the API enabled (last tested version : 0.3.4)
- OBS Studio is running with OBS-Websocket plugin (last tested version : 4.9.0)



Download the latest executable version on [the release section !](https://github.com/Warths/Rocksmith-Scene-Switcher/releases)

Upon first opening of the program, a config.ini file will be created. You can change it, especially the [Behaviour] section


```ini
[OBSWebSocket]
# You can customize OBS WebSocket adress if needed 
host = localhost
port = 4444
pass = 

[RockSniffer]
# You can customize Rocksmith adress if needed 
host = localhost
port = 9938

[Behaviour]
# cooldown refers to the minimum time between two switches. 
# the 3 following values are the scene names tied to its rocksmith state 
# forbidden_switch_on_scenes is the list of the scenes that doesn't allow for automatic changes once inside
cooldown = 3
paused = PauseSceneName
in_game = InGameSceneName
in_menu = MenuSceneName
forbidden_switch_on_scenes = IntroSceneName; OutroSceneName

[Debugging]
# Set Debug to 1 to see various stuff in memory and understand what's going wrong
debug = 0
log_state_interval = 1

```

Have fun !
