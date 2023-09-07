import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form, Query
from loggers import logger
import settings
from fastapi import FastAPI, File, UploadFile, Form
from vectors import create_vector
from apps.schemas import SampleSearchResponse

sample = APIRouter(tags=["样本接口"], prefix='/sample')


def metadata(hash_code: str) -> dict:
    from core.mysql.crud import get_row

    data = get_row(hash_code).dict()

    file_path: str = data['file_path']

    data['file_url'] = f'http://{settings.MINIO_CONFIG.end_point}/image-search-engine/' + \
        file_path.removeprefix('/')

    return data


@sample.post('/file', response_model=list[SampleSearchResponse])
def search_by_file(
    file: UploadFile = File(..., description='DNA文件'),
):
    stream: bytes = file.file.read()
    vector = create_vector(stream)

    from core.milvus.crud import search_vector
    from core.milvus.schemas import SearchResult

    search_results = search_vector(vector)

    return [SampleSearchResponse(**(s.dict() | metadata(s.hash_code))) for s in search_results]
