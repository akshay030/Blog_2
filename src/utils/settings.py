from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    DB_CONNECTION:str
    SECRET_KEY:str
    ALGORITHM:str
    TAVILY_API_KEY:str
    GROQ_API_KEY:str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = 0
    
settings = Settings()