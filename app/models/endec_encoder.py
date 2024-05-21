from typing import Dict, Optional
from enum import Enum
from beanie import Document
from odmantic import ObjectId


class Encoder(Document):
    answer: str
    compressed_text_path:str
    original_size:str
    encoded_size:str
    class Settings:
        name = "encoder"
