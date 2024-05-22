from typing import Dict, Optional
from enum import Enum
from pydantic import BaseModel



class Encoder(BaseModel):
    answer: bytes
    compressed_text_path:str
    original_size:int
    encoded_size:int
