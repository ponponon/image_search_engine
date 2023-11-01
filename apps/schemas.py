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
    file_relative_url: str = Field(...,description='但无法直接访问到 minio 的时候，使用相对路径，让前端对应的 nginx 做代理转发访问 minio')


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


class MetaResult(BaseModel):
    id: int = Field(..., description='mysql 表中的主键自增 id')
    meta_uuid: str = Field(..., description='母本图片的 meta_uuid')
    hash_code: str = Field(..., description='母本图片的 hashcode')
    milvus_id: int = Field(...,
                           description='存储在 milvus 中的 id （是 milvus 的自增 id）')
    file_name: str = Field(..., description='(2.0-distance)/2.0*100')
    file_path: str = Field(..., description='存储在 oss/minio 中的路径')
    created_at: datetime = Field(..., description='图片入库时间')
    updated_at: datetime = Field(..., description='图片最后更新时间')
    file_url: str = Field(...,description='存储在 oss/minio 中的路径，添加 http/https 前缀，允许直接公网访问')
    file_relative_url: str = Field(...,description='但无法直接访问到 minio 的时候，使用相对路径，让前端对应的 nginx 做代理转发访问 minio')


class ListMetaResponse(BaseModel):
    succeed: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='描述')
    data: list[MetaResult] = Field([])
    total: int | None = Field(None, description='表示一共有多少个母本')


class DeleteMetasResponse(BaseModel):
    succeed: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='描述')


class DeleteMetaResponse(BaseModel):
    succeed: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='描述')


class CountMetasResponse(BaseModel):
    succeed: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='描述')
    image_count: int | None = Field(None, description='系统中存储了多少个图片信息')
    vector_count: int | None = Field(None, description='系统中存储了多少个图片向量\
            （图片和向量不是一对一的关系，因为有些图片的 MD5值一样，那么生成的 vector 就会一样，此时系统只会唯一保存一份向量，所有图片和向量之间是多对一关系）\
            。比如存储了十个不一样的图片，那么 image_count 就是 10，vector_count 就是 10；比如存储了十个一样的图片，那么 image_count 就是 10，vector_count 就是 1；\
                比如存储了 5 个图片, A、B C D D，最后两个图片的 md5 值是一模一样的（文件名可以不一样），那么 image_count 就是 5，vector_count 就是 4；')


class GetMetasResponse(BaseModel):
    succeed: bool = Field(..., description='操作是否成功')
    message: str = Field(..., description='描述')
    data: MetaResult | None = Field(None, description='图片母本详情')


class APIConfig(BaseModel):
    upload_minio: bool = Field(True, description='是否把图片上传到 minio 存储桶')
    workers_num: int = Field(1, description='启动多少个工作进程')
    bind_port: int = Field(6200, description='api 接口监听的端口号')
    debug: bool = Field(False, description='是否开启接口调试模式')
    reload: bool = Field(False, description='是否开启接口监听文件变化，即热更新模式')
    version: str = Field('0.0.1', description='api 接口版本')
