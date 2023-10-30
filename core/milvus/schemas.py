from datetime import datetime
from typing import Optional
from pydantic import BaseModel, BaseSettings, Field
from enum import Enum
from numpy import ndarray
from utils.time_helpers import get_utc_now_timestamp
import json


class MilvusSearchConfig(BaseModel):
    threshold: float = Field(...)


# class MilvusIndexParamConfig(BaseModel):
#     index_type: str = Field(...)
#     params: dict = Field(...)
#     metric_type: str = Field(...)

class MilvusIndexConfig(BaseModel):
    name: str = Field(...)
    params: dict = Field(...)


class MilvusCollectionConfig(BaseModel):
    name: str = Field(...)
    search: MilvusSearchConfig = Field(...)
    index: MilvusIndexConfig = Field(...)
    vector_dim: int = Field(...)


class MilvusConfig(BaseModel):
    host: str = Field(...)
    port: str = Field(...)
    database: str = Field('default')
    collection: MilvusCollectionConfig = Field(...)


class MilvusSearchResult(BaseModel):
    id: int = Field(..., description='milvus 的主键')
    distance: float = Field(..., description='汉明距离')
    score: float = Field(..., description='值和汉明距离一模一样')


class MilvusQueryResult(BaseModel):
    id: int = Field(..., description='milvus 的主键')
    video_id: int = Field(..., description='mysql 的主键')
    pts: int = Field(..., description='帧序号，代表几秒')


class MilvusSQResult(BaseModel):
    id: int = Field(..., description='milvus 的主键')
    distance: float = Field(..., description='汉明距离')
    score: float = Field(..., description='值和汉明距离一模一样')
    video_id: int = Field(..., description='mysql 的主键')
    pts: int = Field(..., description='帧序号，代表几秒')


class SampleFrameSearchResult(BaseModel):
    id: int = Field(..., description='milvus 的主键')
    distance: float = Field(..., description='汉明距离')
    score: float = Field(..., description='值和汉明距离一模一样')
    video_uuid: str = Field(..., description='video 的 meta_uuid')
    pts: int = Field(..., description='帧序号，代表几秒')


class SearchResult(BaseModel):
    id: int
    distance: float
    score: float
    hash_code: str
