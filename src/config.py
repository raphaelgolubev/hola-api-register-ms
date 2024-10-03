import os

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


base_dir: str = os.path.dirname(os.path.abspath(__file__))

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


class SecuritySettings(BaseSettings):
    hash_algorithm: str = Field(default="sha256")
    verification_code_expiration_seconds: int = Field(default=1200)

    model_config = ModelConfig(env_prefix='SECURITY_')


class EmailSettings(BaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=25)
    user: str = Field(default="smtp_user")
    password: str = Field(default="smtp_password")
    
    @computed_field
    @property
    def email_templates_dir(self) -> str:
        return os.path.join(os.path.dirname(base_dir), 'static/templates')

    model_config = ModelConfig(env_prefix='EMAIL_')


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
security_settings = SecuritySettings()
email_settings = EmailSettings()
db_settings = DatabaseSettings()