""" function that fetches the configuration parameters form config.yaml"""
import yaml

def get_config():
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    return config
