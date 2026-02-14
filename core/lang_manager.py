from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RuYamlLangModel(BaseModel):
    start: str
    edit_pig_start: str
    edit_pig_process: str
    edit_pig_cancel: str
    edit_pig_error: str
    edit_pig_done: str
    swap_face_start: str
    swap_face_process: str
    swap_face_cancel: str
    swap_face_error: str
    swap_face_done: str


class EnYamlLangModel(BaseModel):
    start: str
    edit_pig_start: str
    edit_pig_process: str
    edit_pig_cancel: str
    edit_pig_error: str
    edit_pig_done: str
    swap_face_start: str
    swap_face_process: str
    swap_face_cancel: str
    swap_face_error: str
    swap_face_done: str


class YamlLangModel(BaseModel):
    ru: RuYamlLangModel
    en: EnYamlLangModel


class LangManager:
    def __init__(self, yaml_path: str = "lang.yaml"):
        self._yaml_path = Path(yaml_path)
        if not self._yaml_path.exists():
            raise FileNotFoundError(f"Config file not found: {self._yaml_path}")

        self._yaml_langmodel = self._load_yaml()

    def _load_yaml(self) -> YamlLangModel:
        with self._yaml_path.open("r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f)

        return YamlLangModel(**data)

    @property
    def ru(self) -> RuYamlLangModel:
        return self._yaml_langmodel.ru
    
    @property
    def en(self) -> RuYamlLangModel:
        return self._yaml_langmodel.en