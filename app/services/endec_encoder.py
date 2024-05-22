import os
import asyncio
import aiofiles
import subprocess
from fastapi import UploadFile, File
from app.models.endec_encoder import Encoder
from app.services.base import BaseService

class CreateEncodedFileService(BaseService):
    async def save_text_file(self, file: UploadFile = File(...)) -> str:
        file_path = os.path.join(os.getcwd(), file.filename.strip())
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()  # Read the file content
            await out_file.write(content)  # Write to the file
        return file_path

    async def execute(self, file: UploadFile) -> dict:
        file_path = await self.save_text_file(file)
        base_name = os.path.splitext(file.filename)[0]
        compressed_file_name = f"{base_name}_compressed.txt"
        compressed_file_path = os.path.join(os.getcwd(), compressed_file_name)

        directory = "/home/heliya/endec/ts_zip-2024-03-02"
        command = f"sudo ./ts_zip --cuda c '{file_path}' '{compressed_file_path}'"
        original_file_size = os.path.getsize(file_path)
        await self.run_command(directory, command)
        compressed_file_size = os.path.getsize(compressed_file_path)

        # Open the file in binary mode ('rb' read binary)
        async with aiofiles.open(compressed_file_path, "rb") as compressed_file:
            compressed_file_content = await compressed_file.read()

        # Encoded answer must be handled as bytes; do not convert to string if unnecessary
        compressed = Encoder(
            answer=compressed_file_content,  # This should be handled as bytes, or encoded appropriately
            original_size=original_file_size,
            compressed_text_path=compressed_file_path,
            encoded_size=compressed_file_size
        )
        os.remove(file_path)  # Clean up the original file
        return compressed.dict()

    async def run_command(self, directory: str, command: str) -> str:
        process = await asyncio.create_subprocess_shell(
            command,
            cwd=directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"Command failed with error: {stderr.decode()}")

        return stdout.decode()
