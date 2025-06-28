import yaml
from networksecurity.exception.exception import NetworkSecurityException
import os,sys
from networksecurity.logging.logger import logging
import numpy as np
import pickle
import dill

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    
    :param file_path: Path to the YAML file.
    :return: Dictionary containing the YAML file content.
    """
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

def write_yaml_file(file_path: str, data: object, replace: bool = False):
    """
    Writes a dictionary to a YAML file.
    
    :param file_path: Path to the YAML file.
    :param data: Dictionary to write to the file.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Removed existing file: {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        logging.info(f"Writing data to YAML file: {file_path}")
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e