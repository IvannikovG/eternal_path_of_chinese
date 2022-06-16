from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Callable


class Job(BaseModel):
    next: Optional[datetime]
    type: str
    name: str
    action: str
    active: bool
    locked: bool


class Translation(BaseModel):
    de: List[str] = []
    en: List[str] = []
    esp: List[str] = []
    ru: List[str] = []


class Examples(BaseModel):
    chinese: Optional[str]
    pinyin: Optional[str]
    translation: Optional[Translation]


class MessageContent(BaseModel):
    hieroglyph_id = str
    chinese: str
    pinyin: str
    translation: Translation
    rule: str = None


class Message(BaseModel):
    examples: Optional[List[Examples]] = None
    resource: MessageContent = {}
    created: str
