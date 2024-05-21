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

        # Save the file asynchronously
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()  # Read the file content
            await out_file.write(content)  # Write to the file
        return file_path

    async def execute(self, file: UploadFile) -> dict:
        print(file)
        """Process the uploaded file, save it, and run the specified command."""
        file_path = await self.save_text_file(file)

        # Extract the base name and create the compressed file name
        base_name = os.path.splitext(file.filename)[0]
        print("base name:",base_name)
        compressed_file_name = f"{base_name}_compressed.txt"
        print("compressed_file_name:",compressed_file_name)
        compressed_file_path = os.path.join(os.getcwd(), compressed_file_name)
        print("compressed_file_path:",compressed_file_path)

        # Define the directory and command
        directory = "/home/heliya/endec/ts_zip-2024-03-02"
        command = f"sudo ./ts_zip --cuda c {file_path} {compressed_file_path}"

        # Get the original file size
        original_file_size = os.path.getsize(file_path)

        # Navigate to the directory and run the command
        result = await self.run_command(directory, command)
        
        # Get the compressed file size
        compressed_file_size = os.path.getsize(compressed_file_path)

        # Read the compressed file content
        async with aiofiles.open(compressed_file_path, "r") as compressed_file:
            compressed_file_content = compressed_file.read()

        # Save the details in the database
        compressed = Encoder(
            answer=str(compressed_file_content,
            compressed_text_path=compressed_file_path,
            original_size=original_file_size,
            encoded_size=compressed_file_size
        )
        # Return the result
        return compressed.dict()

    async def run_command(self, directory: str, command: str) -> str:
        """Run a shell command in a specific directory."""
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
