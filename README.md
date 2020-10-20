# Rocksmith Scene Switcher

Python program that uses Rocksniffer and OBS Web Socket to automatically switch your OBS Studio scene depending on Rocksmith state.

# New Features!

Can we say "new" if it's the first release though ?

  - Supports pausing the game and navigating throught sections
  - Support blacklisting scene from switching (to lock Switcher's depending on the current scene)
  - Supports adding a customizable cooldown between changes
  - Support hot-changes on the config.

# How to use ? 

Go download the latest executable version on [the release section !](https://github.com/Warths/Rocksmith-Scene-Switcher/releases)

Upon first opening of the program, a config.ini file will be created. You can change it, especialy the [Behaviour] section


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
# cooldown refers to the minimum time beetween two switches. 
# the 3 following values are the scene names tied to it's rocksmith state 
# forbidden_switch_on_scenes is the list of the scenes that doesn't allow for automatic changes once inside
cooldown = 3
paused = PauseSceneName
in_game = InGameSceneName
in_menu = MenuSceneName
forbidden_switch_on_scenes = IntroSceneName; OutroSceneName
```

Have fun !
