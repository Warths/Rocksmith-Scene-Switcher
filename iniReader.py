import configparser
from default_config_serialized import serialized
from logger import log
class INIReader:
    def __init__(self, path):
        self.path = path
        self.content = self.load()
        self.save()

    def load(self):
        config = self.get_default()
        config.read(self.path)
        return config

    def reload(self):
        self.content = self.load()

    def save(self):
        with open(self.path, 'w') as configfile:
            self.content.write(configfile)

    def get_default(self):
        config = configparser.ConfigParser()

        for section in serialized:
            config[section] = {}
            for key in serialized[section]:
                config[section][key] = str(serialized[section][key])

        return config

    def get_value(self, section, key, cast=str):
        try:
            if cast == list:
                value = [v.strip() for v in self.content[section][key].split(";")]
            else:
                value = cast(self.content[section][key])
            return value
        except:
            log.notice("Invalid value for {} [{}][{}]. Should be castable into type : {}".format(
                self.path,
                section,
                key,
                str(cast)
            ))
            log.notice("Replacing value with : {}".format(serialized[section][key]))
            self.content[section][key] = serialized[section][key]
            self.save()
            return self.get_value(section, key, cast)



