from typing import Dict, Optional
from enum import Enum
from beanie import Document
from odmantic import ObjectId


class Decoder(Document):
    answer: str
    compressed_file_path:str
    original_size:str
    decoded_size:str
    class Settings:
        name = "decoder"
