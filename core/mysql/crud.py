from core.mysql.models import ImageMetaTable
from core.mysql.schemas import ImageMeta
from playhouse.shortcuts import model_to_dict, update_model_from_dict
from loggers import logger  # TODO
from core.mysql.models import db, ImageMetaTable
from peewee import ModelDelete
from utils.time_helpers import get_utc_now_timestamp, custom_timestamp
from constants import DAY
from playhouse.shortcuts import model_to_dict


def insert_row(
    hash_code: str,
    milvus_id: int,
    file_name: str,
    file_path: str,
    meta_uuid: str
):
    with db.atomic():
        if not ImageMetaTable.get_or_none(meta_uuid=meta_uuid):
            one: ImageMetaTable = ImageMetaTable.create(
                hash_code=hash_code,
                milvus_id=milvus_id,
                file_name=file_name,
                file_path=file_path,
                meta_uuid=meta_uuid
            )
            # two:ImageMetaExtraTable=ImageMetaExtraTable.create(
            #     file_name=file_name, file_path=file_path)


def get_row(
    meta_uuid: str
) -> ImageMeta | None:
    one: ImageMetaTable = ImageMetaTable.get_or_none(
        meta_uuid=meta_uuid)
    if not one:
        return None
    return ImageMeta(**model_to_dict(one))


def get_images_meta_uuids_by_hashcode(hash_code: str) -> list[str]:
    rows = list(ImageMetaTable.select(ImageMetaTable.meta_uuid).where(
        ImageMetaTable.hash_code == hash_code))
    if rows:
        return [row.meta_uuid for row in rows]
    else:
        return []


# def get_rows(
#     hash_code: str
# ) -> list[ImageMeta]:
#     many = ImageMetaTable.filter(
#         hash_code=hash_code
#     )
#     return [ImageMeta(**model_to_dict(row)) for row in many]


# def get_meta_image(hash_code: str) -> ImageMetaTable | None:
#     rows = list(ImageMetaTable.select().where(
#         ImageMetaTable.hash_code == hash_code))
#     if rows:
#         return rows[0]
#     else:
#         return None
