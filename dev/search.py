import os
import shutil
import numpy
import time
from io import BytesIO
import unittest
from loguru import logger
from pathlib import Path
from typing import List
from iv2 import ResNet, l2
from PIL import Image
from core.milvus.models import collection
from core.milvus.crud import insert_vector, has_hash_code, search_vector
from vectors import create_vector
from mark import BASE_DIR
from PIL import UnidentifiedImageError
from utils.md5_helper import get_file_md5
import requests

from concurrent.futures.thread import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=10)


def func():
    try:
        with open('testing/resource/emoji002.jpg', 'rb') as file:
            response = requests.post(
                'http://127.0.0.1:6200/sample/file',
                files={
                    'file': file
                })
            logger.debug(response.text)
            assert response.status_code == 200

    except Exception as error:
        logger.warning(error)


for _ in range(10000):
    pool.submit(func)

pool.shutdown(wait=True)
