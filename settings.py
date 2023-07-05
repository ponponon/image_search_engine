import os
import yaml
from mark import BASE_DIR
from core.mysql.schemas import MysqlConfig
from core.milvus.schemas import MilvusConfig
from core.minio.schemas import MinioConfig
from loguru import logger


run_mode = os.environ.get('RUN_MODE', 'local').lower()

logger.debug(f'当前的运行模式: {run_mode}')


with open(BASE_DIR/'config.yaml', 'r', encoding='utf-8') as f:
    config: dict[str, dict] = yaml.load(f.read(), Loader=yaml.CLoader)
    current_config: dict[str, dict] = config[run_mode]


MYSQL_CONFIG = MysqlConfig(
    **(current_config.get('mysql', {}))
)

MILVUS_CONFIG = MilvusConfig(**(current_config['milvus']))

MINIO_CONFIG = MinioConfig(**(current_config['minio']))


minio_public_base_url = f'http://{MINIO_CONFIG.end_point}/{MINIO_CONFIG.bucket}'
