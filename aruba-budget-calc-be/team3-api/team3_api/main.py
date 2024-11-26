import asyncio
import logging
# from pydantic import UUID4

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from team3_lib.wamp import WampComponent
# from team3_lib.schemas.user import NewUser

log = logging.getLogger(__name__)


class ApiService(WampComponent):
    def __init__(self, config):
        super().__init__(config)

        self.http = FastAPI(title="http REST api", openapi_url="/openapi.json")
        loop = asyncio.get_event_loop()
        fastapi_server = uvicorn.Server(
            config=uvicorn.Config(
                app=self.http, loop=loop, host="0.0.0.0", port=self.settings.port
            )
        )
        loop.create_task(fastapi_server.serve())

        self.allow_origins = config.origins.split(",")

        self.http.add_middleware(
            CORSMiddleware,
            allow_origins=self.allow_origins,
            allow_origin_regex="http://.*:3000",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    async def onJoin(self, details):
        await super().onJoin(details)

        prefix = self.settings.prefix

        # Add endpoints
        self.http.add_api_route(f"{prefix}/ping", endpoint=self.ping)
        self.http.add_api_route(f"{prefix}/pricing", endpoint=self.ping) # to modify with "call_pricing"
        self.http.add_api_route(f"{prefix}/deploy", endpoint=self.ping) # to modify with "call_deploy"

        # self.http.add_api_route(
        #     "/{full_path:path}", endpoint=self.preflight_handler, methods=["OPTIONS"]
        # )
        # self.http.add_api_route(
        #     f"{prefix}/user/get" + "{id_user}",
        #     endpoint=self.get_user,
        #     methods=["GET"],
        # )
        # self.http.add_api_route(
        #     f"{prefix}/user/add",
        #     endpoint=self.add_user,
        #     methods=["POST"],
        # )

    # ====> Endpoints <====
    async def ping(self) -> dict:
        """Tests ping rpc"""
        response = await self.call("ping")
        return {"message": response}

    async def call_pricing(self,
            resource_type_list: list=["computing", "container", "networking", "storage"]
        ):
        """Get prices from catalog and returns json"""

        response = await self.call(
            "get_pricing",
            resource_type_list
        )
    
        return response # {"message": response}
    
    async def call_deploy(self,
            resource_to_deploy: list=[{}]
        ):
        """Deploys resources and returns job outcomes"""

        response = await self.call(
            "deploy_resources",
            resource_to_deploy
        )

        return response


    # async def get_user(self, id_user: UUID4):
    #     """Get user by id"""
    #     response = await self.call("get.user", id_user)
    #     return {"message": response}

    # async def add_user(self, user: NewUser):
    #     """Add a new user"""
    #     print(f"user to add: {user} and {type(user)}")
    #     if isinstance(user, NewUser):
    #         try:
    #             log.info(user.model_dump(mode="json"))
    #             return await self.call("add.user", user.model_dump(mode="json"))
    #         except Exception:
    #             return {
    #                 "message": f"Error when adding the new user {user}",
    #                 "code": 400,
    #             }
    #     else:
    #         return {"message": f"{user} is not a User object", "code": 400}


# ======================
def main():
    from .config import get_config

    service = ApiService(get_config())
    service.run()


if __name__ == "__main__":
    from .config import get_config

    service = ApiService(get_config())
    service.run()
