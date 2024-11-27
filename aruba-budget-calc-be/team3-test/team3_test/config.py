import configargparse
from team3_lib import config


def get_config():
    parser = configargparse.get_argument_parser()
    parser.add_argument("--sleep", default=20)

    return config.general_config(pattern="*team3_test*py")
