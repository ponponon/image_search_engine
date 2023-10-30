from core.mysql.models import db
from pymysql.cursors import Cursor
import threading
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form, Query
from loggers import logger
import settings
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from PIL import Image
import requests
from iv2 import ResNet, l2
from vectors import resnet, distance_2_score
from constants import THRESHOLD

dev = APIRouter(tags=["在线调试和运维接口"], prefix='/dev')


@dev.post('/init', summary='初始化：删除 milvus 和 mysql 中的所有记录')
def init_system():
    try:
        from core.milvus.models import delete_collection, create_model_and_index, load_collection

        delete_collection()

        create_model_and_index()
        load_collection()

        from core.mysql.models import db, model_set
        db.drop_tables(model_set)
        db.create_tables(model_set)

        return JSONResponse(
            {}, status_code=200,
        )
    except Exception as error:
        logger.exception(error)
        return JSONResponse(
            {}, status_code=500,
        )


@dev.post('/flush', summary='milvus 集合 flush')
def flush_milvus():
    try:
        from core.milvus.models import collection

        collection.flush()
        return JSONResponse(
            {}, status_code=200,
        )
    except Exception as error:
        logger.exception(error)
        return JSONResponse(
            {}, status_code=500,
        )


@dev.post('/file_url', summary='刷新 milvus')
def compare_two_by_mutil(
    image_uri_1: str = Form(),
    image_2: bytes = File(),
):

    response = requests.get(image_uri_1)
    file = BytesIO(response.content)
    image_1 = Image.open(file)

    file = BytesIO(image_2)
    image_2 = Image.open(file)

    vector_1 = resnet.gen_vector(image_1)
    vector_2 = resnet.gen_vector(image_2)

    distance = l2(vector_1, vector_2)
    score = distance_2_score(distance, THRESHOLD)

    logger.debug(f'计算得分: {score}')

    return {
        'distance': distance,
        'score': score
    }


@dev.post('/db_reconnect', summary='db_reconnect')
def db_reconnect(
):
    logger.debug(f'当前的线程id: {threading.get_ident()}')
    logger.debug(f'当前的线程id (native): {threading.get_native_id()}')
    with db.cursor() as cursor:
        cursor: Cursor
        sql = """
            SELECT SLEEP(30)
            """.strip()
        cursor.execute(sql)
        cursor.connection.commit()  # 这里必须要提交，不然所有的查询都会处于一个事务中
        rows: tuple[tuple] = cursor.fetchall()

        for row in rows:
            logger.debug(row)


@dev.post('/show_mem', summary='show_mem')
def show_mem(
):
    # import gc
    # import sys

    # def show_memory():
    #     print("*" * 60)
    #     objects_list = []
    #     for obj in gc.get_objects():
    #         size = sys.getsizeof(obj)
    #         objects_list.append((obj, size))
    #     for obj, size in sorted(objects_list, key=lambda x: x[1], reverse=True)[:10]:
    #         print(
    #             f"OBJ: {id(obj)}, TYPE: {type(obj)} SIZE: {size/1024/1024:.2f}MB {str(obj)[:100]}")

    # show_memory()

    # from guppy import hpy

    # h = hpy()

    # # Your code here

    # heap = h.heap()
    # top_10 = heap[:10]
    # print(top_10)

    from mem_top import mem_top

    print(mem_top())

    return {}
