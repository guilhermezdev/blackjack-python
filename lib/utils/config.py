import configparser
import os

class ConfigGame:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(os.getcwd(),'config.cfg')
        self.config.read(self.config_path)
    
    def get_muted(self):
        return self.config.getboolean('config.sound', 'muted')

    def set_muted(self, value):
        self.config.set('config.sound', 'muted', 'yes' if value else 'no')
        self.update_config()

    def update_config(self):
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

game_config = ConfigGame()
