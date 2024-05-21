from fastapi import APIRouter, Body, Depends, Path, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import HTTPException, status

from app.services.endec_encoder import (
CreateEncodedFileService,
)
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Request

router = APIRouter()


@router.post("/fbis/encoder")
async def create_query(request: Request, file: UploadFile):
    service = CreateEncodedFileService()
    created_query = await service.execute(file)
    return created_query
