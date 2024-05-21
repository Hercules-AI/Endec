import os
import asyncio
import aiofiles
import subprocess
from fastapi import UploadFile, File
from app.models.endec_decoder import Decoder
from app.services.base import BaseService

class CreateDecodedFileService(BaseService):
    async def execute(self, compressed_text_path: str) -> dict:
        file_path = compressed_text_path

        # Extract the base name and create the decompressed file name
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        decompressed_file_name = f"{base_name}_decompressed.txt"
        decompressed_file_path = os.path.join(os.getcwd(), decompressed_file_name)
        
        # Define the directory and command
        directory = "/home/heliya/endec/ts_zip-2024-03-02"
        command = f"sudo ./ts_zip --cuda d '{file_path}' '{decompressed_file_path}'"
        # Get the original (compressed) file size
        original_file_size = os.path.getsize(file_path)

        # Navigate to the directory and run the command
        result = await self.run_command(directory, command)

         # Navigate to the directory and run the command
        result = await self.run_command(directory, command)

        # Get the decompressed file size
        decompressed_file_size = os.path.getsize(decompressed_file_path)

        # Read the decompressed file content
        async with aiofiles.open(decompressed_file_path, "r") as decompressed_file:
            decompressed_file_content = await decompressed_file.read()

        # Save the details in the database
        decompressed = Decoder(
            answer=str(decompressed_file_content),
            decompressed_file_path = decompressed_file_path,
            original_size=original_file_size,
            encoded_size=decompressed_file_size
        )
        # Return the result
        return decompressed.dict()

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