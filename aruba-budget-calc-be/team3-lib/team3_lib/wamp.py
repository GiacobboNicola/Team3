import asyncio
import logging
import sys

from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
from autobahn.wamp.types import ComponentConfig
from autobahn.wamp.serializer import JsonSerializer

log = logging.getLogger(__name__)


class WampComponent(ApplicationSession):
    """Wamp class that allow communication via WAMP protocol based on autobahn library project"""

    def __init__(self, config, connect=True):
        ApplicationSession.__init__(self, ComponentConfig(config.realm))
        self.settings = config

        runner = ApplicationRunner(
            url=config.ws, realm=config.realm, serializers=[JsonSerializer()]
        )
        if connect:
            try:
                asyncio.get_event_loop().run_until_complete(
                    runner.run(self, start_loop=False)
                )
            except Exception as ex:
                log.error(f"connection to {config.ws} failed, exit now\nerror:{ex}")
                self.close(force=True)

    async def onJoin(self, details):
        """Join WAMP bus and open communication"""
        log.info(f"wamp session attached to realm {self.settings.realm}")

    def onDisconnect(self):
        """Disconnect and close communication"""
        log.warning("wamp transport lost, shutting down")
        asyncio.get_running_loop().stop()

    def run(self):
        """Starts asyncio loop"""
        asyncio.get_event_loop().run_forever()

    def close(self, force=False):
        try:
            asyncio.get_running_loop().stop()
        except Exception as ex:
            log.error(f"no asyncio loop detected\nerror:{ex}")
        if force:
            log.warning("exit force requested... bye...")
            sys.exit(0)
