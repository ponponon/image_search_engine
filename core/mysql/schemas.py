from pydantic import BaseModel, Field
from datetime import datetime


class MysqlConfig(BaseModel):
    host: str = Field(...)
    port: int = Field(...)
    database_name: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)


class ImageMeta(BaseModel):
    id: int | None
    meta_uuid: str | None
    hash_code: str | None
    milvus_id: int | None
    file_name: str | None
    file_path: str | None
    created_at: datetime | None
    updated_at: datetime | None
