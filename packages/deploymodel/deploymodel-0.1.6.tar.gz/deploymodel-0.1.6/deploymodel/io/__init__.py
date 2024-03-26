from fastapi import File, Form, UploadFile
from pydantic import BaseModel as PydanticBaseModel, Field


class BaseModel(PydanticBaseModel):
    ...


class ModelInput:
    ...


class ModelOutput(BaseModel):
    ...


__all__ = [
    "File",
    "Form",
    "UploadFile",
    "PydanticBaseModel",
    "Field",
    "ModelInput",
    "ModelOutput",
]
