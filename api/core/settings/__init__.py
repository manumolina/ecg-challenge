from core.settings.metadata import app_metadata


class Settings:
    # metadata information
    metadata = app_metadata

    # Environment "local", "dev", "int" or "prod"
    env: str = "local"

    # cors
    cors_allow_origins: str = "*"


settings = Settings()
