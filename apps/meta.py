from fastapi.responses import JSONResponse
from fastapi import APIRouter
from fastapi import Query
from fastapi import FastAPI, File, UploadFile, Form
from vectors import create_vector
from apps.schemas import CreateMetaResponse, ListMetaResponse, DeleteMetasResponse, ListMetaResult, CreateMetaResult
from core.milvus.crud import insert_vector
from core.fs.utils import get_file_extension
from core.fs.utils import get_file_extension
from core.minio.crud import upload
from core.mysql.crud import insert_row
from core.mysql.models import ImageMetaTable
from playhouse.shortcuts import model_to_dict
from utils.md5_helper import get_stream_md5
import settings
from loggers import logger
from utils.time_helpers import timer


meta = APIRouter(tags=["母本接口"], prefix='/meta/image')


@meta.post('/file', response_model=CreateMetaResponse, summary='图片母本入库')
def create_meta_by_file(
    file: UploadFile = File(..., description='图片文件')
):
    with timer('母本入库耗时'):
        try:
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
            logger.debug(f'milvus_id: {milvus_id}')
            insert_row(hash_code, milvus_id, file_name, file_path)

            return CreateMetaResponse(
                succeed=True,
                message=f'母本入库成功',
                data=CreateMetaResult(**{
                    'hash_code': hash_code,
                    'milvus_id': milvus_id,
                    'file_name': file_name,
                    'file_path': file_path
                })
            )
        except Exception as error:
            logger.exception(error)
            return JSONResponse(CreateMetaResponse(
                succeed=False,
                message=f'{str(error)}'
            ).dict(), status_code=500)


@meta.get(
    '',
    response_model=ListMetaResponse,
    summary='列出母本',
    responses={
        200: {
            'model': ListMetaResponse
        },
        500: {
            'model': ListMetaResponse
        },
    }

)
def list_meta(
    offset: int = Query(0),
    limit: int = Query(20),
):
    try:
        _images: list[ImageMetaTable] = list(
            ImageMetaTable.select().offset(offset).limit(limit)
        )

        images = [
            ListMetaResult(**(
                model_to_dict(image) | {
                    'file_url': f'{settings.minio_public_base_url}/{image.file_path}'}
            ))
            for image in _images
        ]
        return ListMetaResponse(
            succeed=True,
            message=f'获取 {len(images)} 个母本',
            data=images
        )
    except Exception as error:
        logger.exception(error)
        return JSONResponse(DeleteMetasResponse(
            succeed=False,
            message=f'{str(error)}'
        ).dict(), status_code=500)


@meta.delete(
    '/images',
    response_model=DeleteMetasResponse,
    summary='删除所有母本',
    responses={
        200: {
            'model': DeleteMetasResponse
        },
        500: {
            'model': DeleteMetasResponse
        },
    }
)
def delete_all_meta(
    recreate_table: bool = Query(False)
):
    try:
        from core.mysql.models import ImageMetaTable, model_set, db
        from core.milvus.models import delete_collection, create_model_and_index, load_collection, collection

        if recreate_table:

            db.drop_tables(model_set)
            db.create_tables(model_set)

            delete_collection()
            create_model_and_index()
            load_collection()

        else:
            ImageMetaTable.delete().where(ImageMetaTable.id > 0).execute()

            expr = f'id > 0'
            logger.debug(expr[:100])
            logger.debug(collection.delete(expr=expr))
            collection.flush()
    except Exception as error:
        logger.exception(error)
        return JSONResponse(DeleteMetasResponse(
            succeed=False,
            message=f'{str(error)}'
        ).dict(), status_code=500)
