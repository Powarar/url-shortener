from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_HOST: str 
    POSTGRES_PORT: int 
    POSTGRES_DB: str 
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"

settings = Settings()