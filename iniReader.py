import configparser
import os

from default_config_serialized import serialized
from logger import log


class INIReader:
    def __init__(self, path):
        self.path = path
        self.content = self.load()

        self.last_modified = self.mtime
        if self.mtime == 0:
            self.save()
            raise FileNotFoundError

    def load(self):
        """
        Load the default config and overwrite it with the config file
        :return: Config Object
        """
        config = self.get_default()
        config.read(self.path, encoding="UTF-8")
        self.last_modified = self.mtime
        return config

    def reload(self):
        """
        Reload only if file changed
        :return: Boolean (True if reloaded else False)
        """

        if self.mtime != self.last_modified:
            self.content = self.load()
            return True
        else:
            return False

    def save(self):
        """
        Write the config to the specified path
        """
        with open(self.path, 'w') as configfile:
            self.content.write(configfile)

    @property
    def mtime(self):
        """ Return last modified time of the config """
        try:
            return os.stat(self.path).st_mtime
        except FileNotFoundError:
            return 0

    def get_default(self):
        """
        get Config Object from the serialized default config
        :return:
        """
        config = configparser.ConfigParser()

        for section in serialized:
            config[section] = {}
            for key in serialized[section]:
                config[section][key] = str(serialized[section][key])

        return config

    def get_value(self, section, key, cast=str):

        try:
            # List in ini are separated with ";". They're also stripped from their spaces
            if cast == list:
                value = [v.strip() for v in self.content[section][key].split(";")]
            # Else we cast it
            else:
                value = cast(self.content[section][key])
            return value
        except:
            # To keep consistency and ease to use for the end user
            # Logging where the value was expected.
            # Replacing it to be sure it's still working even after this error.
            log.notice("Error retrieving value for {} [{}][{}].".format(
                self.path,
                section,
                key,
            ))
            # Getting the new value
            log.notice("Replacing value with : {}".format(serialized[section][key]))
            # Replacing the config value with a default value
            self.content[section][key] = serialized[section][key]
            # Saving the current INI to keep it safe to use
            self.save()
            # Returning new value, using this method
            return self.get_value(section, key, cast)
