import os
import configparser
import yaml

class Config:
    """
    Represents a configuration object that handles reading and writing configuration files.

    Attributes:
        config_path (str): The path to the configuration file.
        config (ConfigParser): The configuration parser object.
        profile (str): The current profile being used.
        AG_EXEC_TIMEOUT (int): The execution timeout value.

    Methods:
        __init__(): Initializes a new instance of the Config class.
        __getattr__(name): Gets called when an attribute with the given name is not found.
        load_config(): Loads the configuration from the file.
        read_config(profile): Reads the configuration for the specified profile.
        write_config(yaml_config, profile): Writes the configuration to the file for the specified profile.
        _write_config(): Writes the configuration to the file.
        _load_config_values(): Loads the configuration values into the class attributes.
    """

    def __init__(self):
        """
        Initializes a new instance of the Config class.

        The configuration file is located in the user's home directory under the '.agent' folder.
        The default profile is set to 'DEFAULT'.
        The default execution timeout is set to 1000 milliseconds.
        """
        home_dir = os.path.expanduser('~')
        config_dir = os.path.join(home_dir, '.agent')
        config_path = os.path.join(config_dir, 'config')
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.profile = 'DEFAULT'
        self.AG_EXEC_TIMEOUT = 1000

        self.load_config()
    
    def __getattr__(self, name):
        """
        Gets called when an attribute with the given name is not found.

        Args:
            name (str): The name of the attribute.

        Raises:
            AttributeError: If the attribute is not found in the configuration file.

        Returns:
            None
        """
        raise AttributeError(f"Please update the config file {self.config_path} profile {self.profile} with the attribute {name}")

    def load_config(self):
        """
        Loads the configuration from the file.

        If the configuration file does not exist, a message is printed.
        Otherwise, the configuration is read for the current profile.
        """
        if not os.path.exists(self.config_path):
            print(f"Config file not found at {self.config_path} Please use the 'write_config' method to create a new config.")
        else:
            self.read_config(self.profile)

    def read_config(self, profile):
        """
        Reads the configuration for the specified profile.

        Args:
            profile (str): The profile to read the configuration for.

        Raises:
            Exception: If an error occurs while reading the configuration.

        Returns:
            None
        """
        try:
            self.profile = profile
            self.config.read(self.config_path)
            self._load_config_values()
        except Exception as e:
            print(f"An error occurred while reading the config: {e}")

    def write_config(self, yaml_config, profile):
        """
        Writes the configuration to the file for the specified profile.

        Args:
            yaml_config (str): The YAML configuration string.
            profile (str): The profile to write the configuration for.

        Raises:
            Exception: If an error occurs while writing the configuration.

        Returns:
            None
        """
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
        """
        Writes the configuration to the file.

        This method is called internally when writing the configuration.
        """
        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)

    def _load_config_values(self):
        """
        Loads the configuration values into the class attributes.

        This method is called internally when reading the configuration.
        """
        for key, value in self.config[self.profile].items():
            setattr(self, key.upper(), value)
        for section in self.config.sections():
            section_dict = getattr(self, section.upper(), {})
            for key, value in self.config[section].items():
                section_dict[key.upper()] = value
            setattr(self, section.upper(), section_dict)

config = Config()