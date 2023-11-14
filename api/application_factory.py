import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import database
from core.settings import settings
from services.ecg.routers.ecg import PATH_PREFIX as ECG_PREFIX
from services.ecg.routers.ecg import ecg_router
from services.user.routers.user import PATH_PREFIX as USER_PREFIX
from services.user.routers.user import users_router

logger = logging.getLogger(__name__)


def create_api() -> FastAPI:

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.cors_allow_origins],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup():
        database.init_db()

    class Tag(str, Enum):
        ECG_API = "ECG"
        AUTHENTICATION_API = "Authentication"
        USER_API = "Users"

    @dataclass
    class ServiceMeta:
        router: APIRouter
        prefix: str
        tag: Tag
        kwargs: dict[str, Any] = field(default_factory=dict)

        def __str__(self) -> str:
            return f"{self.tag.value}: {self.prefix}"

    registered_services = []

    # USERS ADMINISTRATION
    registered_services.append(
        ServiceMeta(
            router=users_router,
            prefix=USER_PREFIX,
            tag=Tag.USER_API,
        ),
    )

    # SOURCE ECG API
    registered_services.append(
        ServiceMeta(
            router=ecg_router,
            prefix=ECG_PREFIX,
            tag=Tag.ECG_API,
        ),
    )

    logger.info(
        "Registered services: %s",
        [str(service) for service in registered_services],
    )

    for service in registered_services:
        app.include_router(
            router=service.router,
            prefix=service.prefix,
            tags=[service.tag],
            **service.kwargs,
        )

    return app
