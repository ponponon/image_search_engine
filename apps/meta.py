import json
from fastapi import APIRouter
from loggers import logger
from fastapi import FastAPI, File, UploadFile, Form
from core.fs.utils import get_file_extension
from vectors import create_vector
from utils.md5_helper import get_stream_md5
from core.milvus.crud import insert_vector
from core.fs.utils import get_file_extension
from core.minio.crud import upload
from core.mysql.crud import insert_row
from core.mysql.models import ImageMetaTable
from playhouse.shortcuts import model_to_dict
import settings
import threading

meta = APIRouter(tags=["母本接口"], prefix='/meta/image')


@meta.post('/file')
def create_meta_by_file(
    file: UploadFile = File(..., description='图片文件'),
):
    stream: bytes = file.file.read()
    extension = get_file_extension(stream)
    hash_code = get_stream_md5(stream)
    logger.debug(file.filename)

    file_name = file.filename or hash_code

    logger.debug(file_name)

    assert extension, f'无效的文件格式, {file.filename}'

    # 上传到 minio
    file_path = f'meta/image/{hash_code}.{extension}'
    upload(stream, file_path)

    vector = create_vector(stream)
    milvus_id = insert_vector(vector, hash_code)

    insert_row(hash_code, milvus_id, file_name, file_path)

    return {
        'hash_code': hash_code,
        'milvus_id': milvus_id,
        'file_name': file_name,
        'file_path': file_path
    }


@meta.get('')
def list_meta():

    images: list[ImageMetaTable] = list(ImageMetaTable.select())

    return [
        model_to_dict(image) | {
            'file_url': f'{settings.minio_public_base_url}/{image.file_path}'}
        for image in images
    ]
