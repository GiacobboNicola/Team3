import logging

import configargparse


def general_config(pattern="*.py"):
    parser = configargparse.get_argument_parser()
    parser.add_argument(
        "--config", required=False, is_config_file=True, help="config file path"
    )
    parser.add_argument(
        "--config-save",
        required=False,
        is_write_out_config_file_arg=True,
        help="config file path",
    )
    parser.add_argument("--debug", action="store_true", default=False, help="debug")
    parser.add_argument("--ws", default="ws://wampbus:18080/ws")
    parser.add_argument("--realm", default="com.team3.demo")
    config = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        level="DEBUG" if config.debug else "INFO",
    )

    if config.debug:
        import jurigged

        jurigged.watch(pattern=pattern)

    return config


def create_transport_config(url):
    config = {"type": "websocket", "url": url, "serializers": ["json"]}
    return config


def create_cryptosign_config(user_id, private_key):
    return {"cryptosign": {"authid": user_id, "privkey": private_key}}


def create_autobahn_component_config(url, realm):
    return {
        "transports": [create_transport_config(url)],
        "authentication": None,
        "realm": realm,
    }
