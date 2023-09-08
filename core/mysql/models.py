import peewee
from datetime import datetime
from peewee import *
import settings
from playhouse.shortcuts import ReconnectMixin


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabase):
    pass


db = ReconnectMySQLDatabase(
    database=settings.MYSQL_CONFIG.database_name,
    host=settings.MYSQL_CONFIG.host,
    port=settings.MYSQL_CONFIG.port,
    user=settings.MYSQL_CONFIG.username,
    password=settings.MYSQL_CONFIG.password,
    charset='utf8mb4'
)


class ImageMetaTable(Model):
    id = AutoField(primary_key=True)
    meta_uuid = CharField(unique=True, max_length=36)
    hash_code = CharField(max_length=36)
    milvus_id = IntegerField()
    file_name = CharField()
    file_path = CharField(help_text='存储在 minio/oss 中的路径')

    created_at = DateTimeField(
        null=False,
        constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')],
        help_text='使用数据库时间'
    )
    updated_at = DateTimeField(
        null=False,
        constraints=[
            SQL('DEFAULT CURRENT_TIMESTAMP'),
            SQL('ON UPDATE CURRENT_TIMESTAMP'),
        ]
    )

    class Meta:
        database = db
        table_name = 'image_meta'


# class ImageMetaExtraTable(Model):
#     id = AutoField(primary_key=True)
#     file_name = CharField()
#     file_path = CharField()

#     created_at = DateTimeField(
#         null=False,
#         constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')],
#         help_text='使用数据库时间'
#     )
#     updated_at = DateTimeField(
#         null=False,
#         constraints=[
#             SQL('DEFAULT CURRENT_TIMESTAMP'),
#             SQL('ON UPDATE CURRENT_TIMESTAMP'),
#         ]
#     )

#     class Meta:
#         database = db
#         table_name = 'image_meta_extra'


model_set: list[Model] = [ImageMetaTable]


if __name__ == '__main__':
    db.drop_tables(model_set)
    db.create_tables(model_set)
