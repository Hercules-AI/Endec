from typing import Dict, Optional
from enum import Enum
from pydantic import BaseModel



class Encoder(BaseModel):
    answer: str
    original_size:int
    encoded_size:int
