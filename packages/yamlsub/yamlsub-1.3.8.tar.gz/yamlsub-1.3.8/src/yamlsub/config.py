from dotenv import load_dotenv
from pyaml_env import parse_config

class Config:
    """Wrapper class for the config.yaml file. It loads the .env file and the config.yaml file and provides methods to access the configuration values.
    """
    def __init__(self, yaml_path='config.yaml', env_path='.env'):
        """Constructor for the Config class. It loads the .env file and the config.yaml file.

        Args:
            yaml_path (str, optional): YAML configuration file. Defaults to 'config.yaml'.
            env_path (str, optional): .env file containing environment variables that may be substituded as values in the YAML configuration file. Defaults to '.env'.
        """
        load_dotenv(env_path, verbose=True, override=True)
        self.__config = parse_config(yaml_path)

    def get_config(self):
        """Retrieve the loaded configuration values.

        Returns:
            dict: configuration values
        """
        return self.__config
    
    def get_config_key(self, key):
        """Retrieve a specific configuration value. Returns None if the key is not found.

        Args:
            key (str): the key of the configuration value to retrieve or None if the key is not found

        Returns:
            object: the value of the configuration key
        """
        return self.__config[key] if key in self.__config else None
