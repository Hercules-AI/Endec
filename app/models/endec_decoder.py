from typing import Dict, Optional
from enum import Enum
from pydantic import BaseModel


class Decoder(BaseModel):
    answer: str
    compressed_file_path:str
    original_size:int
    decoded_size:int
