from pydantic import BaseModel
from typing import List, Optional


class Translation(BaseModel):
    de: List[str] = []
    en: List[str] = []
    esp: List[str] = []
    ru: List[str] = []


class Examples(BaseModel):
    chinese: Optional[str]
    pinyin: Optional[str]
    translation: Optional[Translation]


class Resource(BaseModel):
    hieroglyph_id = str
    chinese: str
    pinyin: str
    translation: Translation
    rule: str = None


class Message(BaseModel):
    examples: Optional[List[Examples]] = None
    resource: Resource = {}
