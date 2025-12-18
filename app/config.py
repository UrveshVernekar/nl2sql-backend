from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/postgres"

    class Config:
        env_file = ".env"


settings = Settings()
