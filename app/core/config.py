from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Todo API"
    DEBUG: bool = True
    VERSION: str = "0.3.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
