from environs import Env

env = Env()

APP_PORT = env.int("APP_PORT")
LOGGER_CONFIG_FILE = env.str("LOGGER_CONFIG_FILE")
