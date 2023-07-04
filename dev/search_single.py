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
import json

import requests

file_apth = '/Users/ponponon/Desktop/code/me/image_search_engine/resources/images/all/0d8cfc85d17f6cf9b58d632ac16ed388.jpg.source.jpg'

with open(file_apth, 'rb') as file:

    response = requests.post(
        'http://127.0.0.1:6200/sample/file',
        files={
            'file': file
        },)

    logger.debug(json.dumps(response.json(), indent=4))


images: list[dict] = response.json()




html = """
<style>
.compare_result{flex-wrap: wrap}
.compare_result img{width:300px}
</style>
"""

for image in images:
    html += f"""
    <p>距离:{image['distance']}</p>
<p>分数:{image['score']}</p>
<div class="compare_result">
<img src="{str(file_apth)}">
<img src="{image['file_path']}">
</div>

<p>------------------------</p>
    """

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html)
