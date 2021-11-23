import os
from configparser import ConfigParser

# Testing if configuration file exists on disk in the current working directory
print("----------")
print("Checking if config file exists -->")
assert os.path.isfile("config.ini") == True
print("OK")
print("----------")

# Opening the configuration file
config = ConfigParser()
config.read('config.ini')

# Checking if all MYSQL related config options are present in the config file
print("Checking if config has MYSQL related options -->")
assert config.has_option('DbConfig', 'db_host') == True
assert config.has_option('DbConfig', 'db') == True
assert config.has_option('DbConfig', 'db_user') == True
assert config.has_option('DbConfig', 'db_pass') == True
print("OK")
print("----------")

# Checking if log config files exist for log config
print("Checking if DB migration component log config file exists dbconfig.yaml -->")
assert os.path.isfile("dbconfig.yaml") == True
print("OK")
print("----------")
print("Checking if log configuration file exists logconfig.yaml -->")
assert os.path.isfile("logconfig.yaml") == True
print("OK")
print("----------")
print("Checking if migration source directory exists -->")
assert os.path.isdir("Migrations") == True
print("OK")
print("----------")
print("Configuration file test DONE -> ALL OK")
print("----------------------------------------")

