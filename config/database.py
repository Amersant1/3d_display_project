import os
from dotenv import load_dotenv

load_dotenv(override=True)


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        error_msg = f"Required variable not found: {name}"
        raise EnvironmentError(error_msg)


DB_USER = get_env_variable("DB_USER")
DB_PASSWORD = get_env_variable("DB_PASSWORD")
DB_HOST = get_env_variable("DB_HOST")
DB_PORT = get_env_variable("DB_PORT")
DB_NAME = get_env_variable("DB_NAME")


DATABASE_CONNECTION_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

