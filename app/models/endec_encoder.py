from pydantic import BaseModel, validator
import base64
class Encoder(BaseModel):
    answer: str
    compressed_text_path: str
    original_size: int
    encoded_size: int

    @validator('answer', pre=True, always=True)
    def convert_bytes_to_base64(cls, v):
        if isinstance(v, bytes):
            return base64.b64encode(v).decode('utf-8')
        return v