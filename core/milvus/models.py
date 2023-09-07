import settings
from pymilvus import (
    connections,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
)
from loggers import logger

from pymilvus import DataType


connections.connect(
    host=settings.MILVUS_CONFIG.host,
    port=settings.MILVUS_CONFIG.port,
)

schema = CollectionSchema([
    FieldSchema("id", DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema("hash_code", DataType.VARCHAR, max_length=64),
    FieldSchema("image_vector", dtype=DataType.FLOAT_VECTOR,
                dim=512)
])

# 集合不存在，则会自动创建集合；已存在，不会重复创建
collection = Collection(settings.MILVUS_CONFIG.collection.name, schema)


# 索引不存在，则会自动创建索引；已存在，不会重复创建

# logger.debug(settings.MILVUS_CONFIG.collection.index.params)


def create_model_and_index():
    collection = Collection(settings.MILVUS_CONFIG.collection.name, schema)

    if not collection.has_index(index_name='index_vector'):
        collection.create_index(
            field_name=settings.MILVUS_CONFIG.collection.index.name,
            index_params=settings.MILVUS_CONFIG.collection.index.params,
            index_name="index_vector"
        )

    if not collection.has_index(index_name='index_hash_code'):
        collection.create_index(
            field_name='hash_code',
            index_name="index_hash_code"
        )


def load_collection():
    collection.load()


def delete_collection():
    from pymilvus import utility
    from core.milvus.models import connections

    connections.connect(
        host=settings.MILVUS_CONFIG.host,
        port=settings.MILVUS_CONFIG.port,
    )
    collections: list[str] = utility.list_collections()
    if settings.MILVUS_CONFIG.collection.name in collections:
        utility.drop_collection(settings.MILVUS_CONFIG.collection.name)


create_model_and_index()
load_collection()
