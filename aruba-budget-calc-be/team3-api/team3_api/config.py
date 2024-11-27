import configargparse
from team3_lib import config


def get_config():
    parser = configargparse.get_argument_parser()
    parser = configargparse.get_argument_parser()
    parser.add_argument("--prefix", default="/api")
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="http listen port",
    )
    parser.add_argument("--origins", default="http://172.*:8100,http://localhost:8100")

    return config.general_config(pattern="*team3_api*py")
