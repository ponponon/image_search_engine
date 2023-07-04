from pydantic import BaseModel


class MinioConfig(BaseModel):
    access_key: str
    secret_key: str
    end_point: str
    bucket: str
