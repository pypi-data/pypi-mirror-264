import json
from typing import Tuple

class Config:
    project_name: str = ''
    src_dir: str = 'src'
    dist_dir: str = 'dist'
    build_dir: str = 'build'
    version: str = '0.0.0'
    engine: str = ''
    scripts: dict = {}

    @staticmethod
    def load(log: bool = True) -> bool:
        try:
            with open('.proj.config', 'r') as config_file:
                config_json = json.load(config_file)
                for key, value in config_json.items():
                    setattr(Config, key, value)
            return True
        except FileNotFoundError:
            if log:
                print('Config file not found. Default values will be used.')
            return False

    @staticmethod
    def save():
        
        config_json = {}
        for attr_name in set(dir(Config)):
            if attr_name.startswith('__'):
                continue

            attr_value = getattr(Config, attr_name)            
            attr_type = type(attr_value)

            if attr_type in [type(Config.load), type]:
                continue

            config_json[attr_name] = attr_value
        with open('.proj.config', 'w') as config_file:
            json.dump(config_json, config_file, indent=4)

    @staticmethod
    def add_engine_specific_config_group(group_name: str, group: dict):
        setattr(Config, group_name, group)

    @staticmethod
    def read_engine_specific_config_group(group_name: str) -> dict:
        return getattr(Config, group_name, {})

Config.load()