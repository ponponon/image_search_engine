import os
from pathlib import Path
from loguru import logger
from PIL import UnidentifiedImageError
import requests
from mark import BASE_DIR


images_dir: Path = BASE_DIR/'resources/images/all'

images_dir: Path = Path('/home/pon/Pictures')
images_dir: Path = Path(
    '/home/pon/Downloads/iv测试图片集')


def get_file_size(file_path: Path) -> int:
    return os.path.getsize(file_path)


formats = ('jpg', 'jpeg', 'png')

images = [images_dir /
          f for f in os.listdir(images_dir) if f.endswith(formats) and not f.startswith('.')]

images.sort()

logger.debug(f'一共有 {len(images)} 个图片')

for index, image in enumerate(images):
    try:
        logger.debug(f'{index}/{len(images)-1} {image.name}')

        with open(image, 'rb') as file:
            response = requests.post(
                'http://127.0.0.1:6200/meta/image/file',
                files={
                    'file': file
                },)
            assert response.status_code == 200

    except (UnidentifiedImageError, OSError) as error:
        logger.warning(error)
        os.remove(image)
    except Exception as error:
        logger.exception(error)
