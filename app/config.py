from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Commitment Radar"
    app_env: str = "development"
    port: int = 8000
    public_base_url: str = "http://127.0.0.1:8000"
    webhook_secret: str = "dev-only-change-me"
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    qdrant_collection: str = "commitment_radar"
    lyzr_api_key: str = ""
    lyzr_agent_id: str = ""
    lyzr_api_base_url: str = ""
    omi_webhook_secret: str = ""
    qloo_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

settings = Settings()
