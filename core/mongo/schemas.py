from pydantic import BaseModel, Field


class MongoConfig(BaseModel):
    host: str = Field(...)
    port: int = Field(...)
    db_name: str
    collection_name: str
