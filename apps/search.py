import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form, Query
from fastapi import FastAPI, File, UploadFile, Form
from vectors import create_vector
from core.milvus.crud import search_vector
from playhouse.shortcuts import model_to_dict
from core.mysql.crud import get_meta_image
import settings

search = APIRouter(tags=["搜索引擎的调试接口"], prefix='/search')


def add_meta_image_info(hash_code: str) -> dict:

    meta_image = get_meta_image(hash_code)
    if not meta_image:
        return {}

    return model_to_dict(meta_image) | {'file_url': f'{settings.minio_public_base_url}/{meta_image.file_path}'}


@search.post('', summary='样本搜索接口，查询相似的图片母本')
def search_sample(
    sample_image: UploadFile = File(),
    limit: int = Form(100)
):
    file = sample_image.file
    vector = create_vector(file)
    search_results = search_vector(vector, limit)

    return [
        s.dict() | add_meta_image_info(s.hash_code)
        for s in search_results
    ]
