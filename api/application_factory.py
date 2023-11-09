import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings
from core.database import init_db

from services.ecg.routers.default import ecg_router

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
        init_db()

    class Tag(str, Enum):
        ECG_API = "ECG"
        AUTHENTICATION_API = "Authentication API"

    @dataclass
    class ServiceMeta:
        router: APIRouter
        prefix: str
        tag: Tag
        kwargs: dict[str, Any] = field(default_factory=dict)

        def __str__(self) -> str:
            return f"{self.tag.value}: {self.prefix}"

    registered_services = []

    # SOURCE ECG API
    registered_services.append(
        ServiceMeta(
            router=ecg_router,
            prefix="/sources/ecg",
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
