from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    pg_host: str
    pg_port: int
    pg_database: str
    pg_user: str
    pg_password: str
    jwt_secret: str
    jwt_expiration: int
    jwt_algorithm: str
    jwt_issuer: str
    admin_key: str

    model_config = SettingsConfigDict(env_file=".env")