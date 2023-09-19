from core.mysql.crud import get_images_meta_uuids_by_hashcode
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form, Query
from loggers import logger
import settings
from fastapi import FastAPI, File, UploadFile, Form
from vectors import create_vector
from apps.schemas import SearchSampleResponse, SearchSampleResult
from utils.time_helpers import timer


sample = APIRouter(tags=["样本接口"], prefix='/sample')


def metadata(meta_uuid: str) -> dict:
    from core.mysql.crud import get_row

    data = get_row(meta_uuid).dict()

    file_path: str = data['file_path']

    data['file_url'] = f'http://{settings.MINIO_CONFIG.end_point}/image-search-engine/' + \
        file_path.removeprefix('/')

    return data


@sample.post('/file', response_model=SearchSampleResponse, summary='图片查询', responses={
    200: {
        'model': SearchSampleResponse
    },
    500: {
        'model': SearchSampleResponse
    },
})
def search_by_file(
    file: UploadFile = File(..., description='图片文件'),
    offset: int = Form(0, description='用于控制翻页, 表示起始位置'),
    limit: int = Form(100, description='表示返回搜索最相似的 N 个'),

):
    with timer('样本查询耗时'):
        try:
            stream: bytes = file.file.read()
            vector = create_vector(stream)

            from core.milvus.crud import search_vector
            from core.milvus.schemas import SearchResult

            search_results = search_vector(vector, offset, limit)

            data = []

            for search_result in search_results:
                images_meta_uuids = get_images_meta_uuids_by_hashcode(
                    search_result.hash_code)
                for image_meta_uuid in images_meta_uuids:
                    data.append(SearchSampleResult(
                        **(search_result.dict() | metadata(image_meta_uuid))))

            return SearchSampleResponse(
                succeed=True,
                message=f'获取 {len(data)} 个母本',
                data=data
            )
        except Exception as error:
            logger.exception(error)
            return JSONResponse(SearchSampleResponse(
                succeed=False,
                message=f'{str(error)}'
            ).dict(), status_code=500)
