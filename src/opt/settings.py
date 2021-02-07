import os
import configparser

print(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read(["../config.ini", "../hidden.ini"])
