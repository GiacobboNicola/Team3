import logging
import time

from team3_lib.wamp import WampComponent

log = logging.getLogger(__name__)


class CoreService(WampComponent):
    def __init__(self, config):
        super().__init__(config)

    #        asyncio.get_event_loop().run_until_complete(database.session.init(config))

    async def onJoin(self, details):
        await super().onJoin(details)
        # register(s)
        await self.register(self.ping, "ping")

        # subscription(s)
        self.subscribe(self.show_ping, "test.ping")

    # procedures
    async def ping(self):
        log.debug({"message": "ping", "time": time.time()})
        return {"message": "pong", "time": time.time()}

    async def show_ping(self, ping=None):
        log.info(f"from test->core: {ping}")


# ======================
# def create_tables():
#     from .config import get_config

#     asyncio.get_event_loop().run_until_complete(
#         database.session.init(get_config(), create=True)
#     )


def main():
    from .config import get_config

    service = CoreService(get_config())
    service.run()
