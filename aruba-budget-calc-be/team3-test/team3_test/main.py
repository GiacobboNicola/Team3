import logging
import time

from team3_lib.wamp import WampComponent

log = logging.getLogger(__name__)


class TestService(WampComponent):
    def __init__(self, config):
        super().__init__(config)

    async def onJoin(self, details):
        await super().onJoin(details)

        time.sleep(self.settings.sleep)
        response = await self.call("ping")
        log.info(response)
        self.publish("test.ping", ping=response)

        self.close()


# ======================
def main():
    from .config import get_config

    service = TestService(get_config())
    service.run()
