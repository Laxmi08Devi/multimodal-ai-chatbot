from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multimodal AI Chatbot"
    database_url: str = "postgresql://postgres:password@localhost:5432/multimodal_ai"

    openai_api_key: str = ""
    openai_model: str = "gpt-5.6-luna"
    embedding_model: str = "text-embedding-3-small"

    upload_dir: str = "uploads"
    generated_dir: str = "generated"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()