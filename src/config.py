from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig:
    def __new__(cls, *args, **kwargs):
        config = SettingsConfigDict(
            extra="ignore",
            validate_default=False,
            case_sensitive=False,
            env_ignore_empty=True,
            env_file_encoding='utf-8',
            env_file='.env'
        )
        config.update(**kwargs)
        return config


class AppSettings(BaseSettings):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    model_config = ModelConfig(env_prefix='APP_')


class DatabaseSettings(BaseSettings):
    host: str = Field(default="localhost")
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    db: str = Field(default="postgres")
    port: int = Field(default=5432)

    @property
    def sync_dsn(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def async_dsn(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    model_config = ModelConfig(env_prefix='POSTGRES_')


app_settings = AppSettings()
db_settings = DatabaseSettings()