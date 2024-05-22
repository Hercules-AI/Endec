import os
import asyncio
import aiofiles
import subprocess
import base64
from fastapi import UploadFile, File
from app.models.endec_decoder import Decoder
from app.services.base import BaseService

class CreateDecodedFileService(BaseService):
    async def save_text_file(self, file: UploadFile = File(...)) -> str:
        # Assume the content you receive is base64 encoded
        content = await file.read()
        decoded_content = base64.b64decode(content)  # Decode Base64 to bytes

        file_path = os.path.join(os.getcwd(), file.filename.strip())
        # Save the decoded binary data asynchronously
        async with aiofiles.open(file_path, "wb") as out_file:
            await out_file.write(decoded_content)  # Write the binary data
        return file_path

    async def execute(self, file: UploadFile) -> dict:
        file_path = await self.save_text_file(file)
        base_name = os.path.splitext(file.filename)[0]
        decompressed_file_name = f"{base_name}_decompressed.txt"
        decompressed_file_path = os.path.join(os.getcwd(), decompressed_file_name)
        
        directory = "/home/heliya/endec/ts_zip-2024-03-02"
        command = f"sudo ./ts_zip --cuda d '{file_path}' '{decompressed_file_path}'"
        original_file_size = os.path.getsize(file_path)

        # Ensure the command is run only once
        result = await self.run_command(directory, command)

        decompressed_file_size = os.path.getsize(decompressed_file_path)

        async with aiofiles.open(decompressed_file_path, "r") as decompressed_file:
            decompressed_file_content = await decompressed_file.read()

        decompressed = Decoder(
            answer=str(decompressed_file_content),
            original_size=original_file_size,
            decompressed_file_path=decompressed_file_path,
            decoded_size=decompressed_file_size
        )
        os.remove(file_path)  # Clean up the original file

        return decompressed.dict()

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

