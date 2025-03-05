import os
from dotenv import load_dotenv

load_dotenv(override=True)


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        error_msg = f"Required variable not found: {name}"
        raise EnvironmentError(error_msg)






WEBHOOK_PORT = get_env_variable("WEBHOOK_PORT")