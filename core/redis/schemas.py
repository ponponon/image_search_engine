from pydantic import BaseModel, Field


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int
    key: str | None
