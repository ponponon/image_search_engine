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


resnet: ResNet = ResNet(
    weight_file='weight/gl18-tl-resnet50-gem-w-83fdc30.pth'
)

images_dir: Path = BASE_DIR/'resources/images/all'


def get_file_size(file_path: Path) -> int:
    return os.path.getsize(file_path)


formats = ('jpg', 'jpeg', 'png')

images = [images_dir /
          f for f in os.listdir(images_dir) if f.endswith(formats)]

logger.debug(f'一共有 {len(images)} 个图片')
logger.debug(f'开始构建mapping')
mapping = {}

for image in images:
    hash_code = get_file_md5(image)
    mapping[hash_code] = str(image)
logger.debug(f'构建mapping完成')

src_image = Path(
    '/Users/ponponon/Desktop/code/me/image_search_engine/resources/images/all/zidanfei10428.jpg')

hit_images = search_vector(resnet.gen_vector(src_image), 10000)
logger.debug(f'搜索完毕')
html = """
<style> 
.compare_result{flex-wrap: wrap} 
.compare_result img{width:300px} 
</style> 
"""

for hit_image in hit_images:
    html += f"""
    <p>距离:{hit_image.distance}</p>
<p>分数:{hit_image.score}</p>
<div class="compare_result">
<img src="{str(src_image)}">
<img src="{mapping[hit_image.hash_code]}">
</div>

<p>------------------------</p>
    """

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html)
