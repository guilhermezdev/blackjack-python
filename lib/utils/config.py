import configparser
import os

class ConfigGame:
    def __init__(self):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.getcwd(),'config.cfg')
        self.config.read(config_path)
    
    def get_muted(self):
        return self.config.getboolean('config.sound', 'muted')

    def set_muted(self, value):
        self.config.set('config.sound', 'muted', 'yes' if value else 'no')

game_config = ConfigGame()
