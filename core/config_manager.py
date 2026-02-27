from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotYamlConfig(BaseModel):
    name: str
    main_group_url: str
    address_keywords: list[str]
    eavesdrop_cooldown: int
    eavesdrop_chance: int
    eavesdrop_finance_triggers: list[str]
    eavesdrop_aggression_triggers: list[str]


class AiYamlConfig(BaseModel):
    chat_model: str
    chat_system_prompt: str
    eavesdrop_system_prompt: str
    temperature: float
    max_tokens: int
    edit_image_system_prompt: str
    face_swap_system_prompt: str
    image_model: str
    image_size: str
    quality: str
    reference_image: str


class YamlConfig(BaseModel):
    bot: BotYamlConfig
    ai: AiYamlConfig


class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    telegram_bot_token: str = Field(alias="TELEGRAM_BOT_TOKEN")
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
    def bot(self) -> BotYamlConfig:
        return self._yaml_config.bot
    
    @property
    def ai(self) -> AiYamlConfig:
        return self._yaml_config.ai

    @property
    def telegram_bot_token(self) -> str:
        return self._env_config.telegram_bot_token
    
    @property
    def proxy_api_key(self) -> str:
        return self._env_config.proxy_api_key