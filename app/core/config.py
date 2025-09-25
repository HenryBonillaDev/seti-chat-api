from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    system_responses: bool = True
    xai_api_key: str
    database_url: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()
