import json
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "student_management"
    DB_USER: str = "root"
    DB_PASSWORD: str = "your_password"
    CORS_ORIGINS: str = '["http://localhost:5173"]'
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 5242880

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def cors_origins_list(self) -> list[str]:
        return json.loads(self.CORS_ORIGINS)

settings = Settings()