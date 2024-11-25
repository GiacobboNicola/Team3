import configargparse

from team3_lib import config


def get_config():
    parser = configargparse.get_argument_parser()
    parser.add_argument(
        "--db",
        default="postgresql+asyncpg://root@node_1:26257/team3?ssl=disable",
    )

    return config.general_config(pattern="*team3_core*py")
