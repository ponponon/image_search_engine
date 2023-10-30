import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form, Query
from loggers import logger
import settings

milvus = APIRouter(tags=["milvus 的调试和运维接口"], prefix='/milvus')


@milvus.post('/', summary='milvus 健康检查接口')
def flush_milvus():
    try:
        return JSONResponse(
            {}, status_code=200,
        )
    except Exception as error:
        logger.exception(error)
        return JSONResponse(
            {}, status_code=500,
        )


@milvus.post('/flush', summary='刷新 milvus')
def flush_milvus():
    from core.milvus.models import milvus
    milvus.flush(collection_names=[settings.MILVUS_CONFIG.collection.name])
    return True


# @milvus.post('/rebuild_vector_index', summary='重建 milvus 集合的向量索引')
# def rebuild_vector_index(): #TODO: https://github.com/milvus-io/pymilvus/issues/1733
#     from core.milvus.models import collection, connections

#     collection.create_index

#     milvus.flush(collection_names=[settings.MILVUS_CONFIG.collection.name])
#     return True
