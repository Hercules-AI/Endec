from pydantic import BaseModel, Field
from typing import Optional
import base64

class Encoder(BaseModel):
    answer: str
    compressed_text_path: str
    original_size: int
    encoded_size: int
    raw_data: Optional[bytes] = Field(None, exclude=True)  # Hold the raw binary data, exclude from responses

    @property
    def answer(self) -> str:
        """Encode the raw binary data as base64 when accessing the answer field."""
        if self.raw_data is not None:
            return base64.b64encode(self.raw_data).decode('utf-8')
        return ""

    @answer.setter
    def answer(self, value: bytes):
        """Store raw data when setting the answer field."""
        self.raw_data = value