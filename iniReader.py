import configparser
from default_config_serialized import serialized
from logger import log

class INIReader:
    def __init__(self, path):
        self.path = path
        self.content = self.load()
        self.save()

    def load(self):
        """
        Load the default config and overwrite it with the config file
        :return: Config Object
        """
        config = self.get_default()
        config.read(self.path)
        return config

    def reload(self):
        self.content = self.load()

    def save(self):
        """
        Write the config to the specified path
        """
        with open(self.path, 'w') as configfile:
            self.content.write(configfile)

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



