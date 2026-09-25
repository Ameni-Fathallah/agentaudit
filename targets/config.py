"""Configuration des agents cibles, chargée depuis le fichier .env."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class TargetSettings(BaseSettings):
    """Paramètres communs à tous les agents cibles."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ollama_base_url: str = "http://localhost:11434"
    target_model: str = "llama3.2:3b"
    embedding_model: str = "bge-m3"
    vector_store_path: str = "vector_store"
    rag_top_k: int = 4


settings = TargetSettings()
