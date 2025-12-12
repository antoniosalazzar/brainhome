from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # Application settings
    APP_NAME: str = "HomeBrain Core API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    # DB settings (PostgreSQL)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "homebrain_user"
    DB_PASSWORD: str = "securepassword"
    DB_NAME: str = "homebrain_db"

    # Security JWT
    SECRET_KEY: str = "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings (for future frontend integration)
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Environment settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    @property
    def DATABASE_URL(self) -> str:
        """Construye la URL de base de datos dinámicamente"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()