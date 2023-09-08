from datetime import datetime
from typing import Optional
from pydantic import BaseModel, BaseSettings, Field
from enum import Enum
from numpy import ndarray
from utils.time_helpers import get_utc_now_timestamp
import json


class SearchSampleResult(BaseModel):
    id: int = Field(..., description='mysql 表中的主键自增 id')
    distance: float = Field(
        ..., description='l2 欧式距离（不开根号的），用于衡量两个向量的相似度，越接近 0 越相似，在本次算法中，一般距离在 0.25 之类，都是比较可靠的')
    score: float = Field(..., description='(2.0-distance)/2.0*100')
    meta_uuid: str = Field(..., description='母本图片的 meta_uuid')
    hash_code: str = Field(..., description='母本图片的 hashcode')
    milvus_id: int = Field(...,
                           description='存储在 milvus 中的 id （是 milvus 的自增 id）')
    file_name: str = Field(..., description='(2.0-distance)/2.0*100')
    file_path: str = Field(..., description='存储在 oss/minio 中的路径')
    created_at: datetime = Field(..., description='图片入库时间')
    updated_at: datetime = Field(..., description='图片最后更新时间')
    file_url: str = Field(...,
                          description='存储在 oss/minio 中的路径，添加 http/https 前缀，允许直接公网访问')


class SearchSampleResponse(BaseModel):
    succeed: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='描述')
    data: list[SearchSampleResult] = Field([])


class CreateMetaResult(BaseModel):
    meta_uuid: str = Field(..., description='母本图片的 meta_uuid')
    hash_code: str = Field(..., description='母本图片的 hashcode')
    milvus_id: int = Field(...,
                           description='存储在 milvus 中的 id （是 milvus 的自增 id）')
    file_name: str = Field(..., description='(2.0-distance)/2.0*100')
    file_path: str = Field(..., description='存储在 oss/minio 中的路径')


class CreateMetaResponse(BaseModel):
    succeed: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='描述')
    data: CreateMetaResult | None


class CreateMeta500ResponseTemplate(BaseModel):
    succeed: bool = Field(False, description='操作失败')
    message: str = Field(..., description='失败描述')
    data: None = Field(None, description='失败描述')


class ListMetaResult(BaseModel):
    id: int = Field(..., description='mysql 表中的主键自增 id')
    meta_uuid: str = Field(..., description='母本图片的 meta_uuid')
    hash_code: str = Field(..., description='母本图片的 hashcode')
    milvus_id: int = Field(...,
                           description='存储在 milvus 中的 id （是 milvus 的自增 id）')
    file_name: str = Field(..., description='(2.0-distance)/2.0*100')
    file_path: str = Field(..., description='存储在 oss/minio 中的路径')
    created_at: datetime = Field(..., description='图片入库时间')
    updated_at: datetime = Field(..., description='图片最后更新时间')
    file_url: str = Field(...,
                          description='存储在 oss/minio 中的路径，添加 http/https 前缀，允许直接公网访问')


class ListMetaResponse(BaseModel):
    succeed: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='描述')
    data: list[ListMetaResult] = Field([])


class DeleteMetasResponse(BaseModel):
    succeed: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='描述')
