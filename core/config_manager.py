from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppYamlConfig(BaseModel):
    name: str


class AiYamlConfig(BaseModel):
    chat_system_promt: str
    chat_model: str
    temperature: float
    max_tokens: int


class YamlConfig(BaseModel):
    app: AppYamlConfig
    ai: AiYamlConfig


class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    telegram_bot_token: str = Field(alias="TELEGRAM_BOT_TOKEN")
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    proxy_api_key: str = Field(alias="PROXYAPI_API_KEY")


class Config:
    def __init__(self, yaml_path: str = "config.yaml"):
        self._yaml_path = Path(yaml_path)

        if not self._yaml_path.exists():
            raise FileNotFoundError(f"Config file not found: {self._yaml_path}")

        self._yaml_config = self._load_yaml()
        self._env_config = EnvConfig()

    def _load_yaml(self) -> YamlConfig:
        with self._yaml_path.open("r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f)

        return YamlConfig(**data)

    @property
    def app(self) -> AppYamlConfig:
        return self._yaml_config.app
    
    @property
    def ai(self) -> AiYamlConfig:
        return self._yaml_config.ai

    @property
    def telegram_bot_token(self) -> str:
        return self._env_config.telegram_bot_token
    
    @property
    def openai_api_key(self) -> str:
        return self._env_config.openai_api_key
    
    @property
    def proxy_api_key(self) -> str:
        return self._env_config.proxy_api_key