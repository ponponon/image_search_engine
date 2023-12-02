from pydantic import BaseModel


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int
    key: str | None
