from fastapi import APIRouter, Body, Depends, Path, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import HTTPException, status

from app.services.endec_decoder import (
CreateDecodedFileService,
)
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Request

router = APIRouter()


@router.post("/fbis/decoder")
async def create_query(request: Request,compressed_file_path: str = Body(...)):
    service = CreateDecodedFileService()
    created_query = await service.execute(compressed_file_path)
    return created_query
