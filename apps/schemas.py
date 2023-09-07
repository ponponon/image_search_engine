from datetime import datetime
from typing import Optional
from pydantic import BaseModel, BaseSettings, Field
from enum import Enum
from numpy import ndarray
from utils.time_helpers import get_utc_now_timestamp
import json


class SampleSearchResponse(BaseModel):
    id: int = Field(..., description='mysql 表中的主键自增 id')
    distance: float = Field(
        ..., description='l2 欧式距离（不开根号的），用于衡量两个向量的相似度，越接近 0 越相似，在本次算法中，一般距离在 0.25 之类，都是比较可靠的')
    score: float
    hash_code: str
    milvus_id: int
    file_name: str
    file_path: str
    created_at: datetime
    updated_at: datetime
    file_url: str
