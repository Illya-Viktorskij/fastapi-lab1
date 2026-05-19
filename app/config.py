from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    database_url: str
    test_database_url: str = ""
    secret_key: str
    grafana_password: str = "admin"


settings = Settings()