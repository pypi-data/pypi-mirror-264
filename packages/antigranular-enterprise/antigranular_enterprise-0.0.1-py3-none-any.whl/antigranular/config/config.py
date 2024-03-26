import os
import configparser
import yaml

class Config:
    def __init__(self):
        home_dir = os.path.expanduser('~')
        config_dir = os.path.join(home_dir, '.agent')
        config_path = os.path.join(config_dir, 'config')
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.profile = 'DEFAULT'
        self.AG_EXEC_TIMEOUT = 1000

        if not os.path.exists(self.config_path):
            os.makedirs(config_dir, exist_ok=True)
        else:
            self.read_config(self.profile)

    def read_config(self, profile):
        try:
            self.profile = profile
            self.config.read(self.config_path)
            self._load_config_values()
        except Exception as e:
            print(f"An error occurred while reading the config: {e}")

    def write_config(self, yaml_config, profile):
        try:
            self.profile = profile
            config_dict = yaml.safe_load(yaml_config)
            self.config[self.profile] = config_dict
            with open(self.config_path, 'w') as config_file:
                self.config.write(config_file)
            self._load_config_values()
        except Exception as e:
            print(f"An error occurred while writing the config: {e}")


    def _write_config(self):
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)

    def _load_config_values(self):
        for key, value in self.config[self.profile].items():
            setattr(self, key.upper(), value)
        for section in self.config.sections():
            section_dict = getattr(self, section.upper(), {})
            for key, value in self.config[section].items():
                section_dict[key.upper()] = value
            setattr(self, section.upper(), section_dict)