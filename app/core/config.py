from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Todo API"
    DEBUG: bool = True
    VERSION: str = "0.3.0"
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()
