import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form, Query
from loggers import logger
import settings
from fastapi import FastAPI, File, UploadFile, Form
from vectors import create_vector

sample = APIRouter(tags=["样本接口"], prefix='/sample')


def metadata(hash_code: str) -> dict:
    from core.mysql.crud import get_row

    data = get_row(hash_code).dict()

    file_path: str = data['file_path']

    data['file_path'] = 'http://192.168.31.245:9000/image-search-engine/' + \
        file_path.removeprefix('/')

    return data


@sample.post('/file')
def search_by_file(
    file: UploadFile = File(..., description='DNA文件'),
):

    stream: bytes = file.file.read()
    vector = create_vector(stream)

    from core.milvus.crud import search_vector
    from core.milvus.schemas import SearchResult

    search_results = search_vector(vector)

    return [s.dict() | metadata(s.hash_code) for s in search_results]


@sample.post('/web/file')
def search_by_file(
    file: UploadFile = File(..., description='DNA文件'),
):

    stream: bytes = file.file.read()
    vector = create_vector(stream)

    from core.milvus.crud import search_vector
    from core.milvus.schemas import SearchResult

    search_results = search_vector(vector)

    return [s.dict() for s in search_results]
