from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "python template"
    DEBUG: bool = True

    TEMPO_EXPORTER: str
    LOKI_URL: str

    # Kafka Ecosystem
    KAFKA_CONNECT_URL: str
    SCHEMA_REGISTRY_URL: str
    KAFKA_REST_PROXY_URL: str
    KAFKA_BROKERS: list[str]

    # Search & AI
    OPENSEARCH_URL: str
    OLLAMA_URL: str

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT_WRITE: int
    DB_PORT_READ: int
    DB_NAME: str

    # Redis & Automation
    REDIS_URL: str
    N8N_URL: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
