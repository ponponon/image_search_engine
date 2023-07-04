from pathlib import Path
from core.minio.models import client, bucket
import settings
from io import BytesIO
from core.fs.utils import get_file_mime


def download(file_path: str) -> bytes:
    return bucket.get_object(file_path).read()


def exist(file_path: str) -> bool:
    objects = client.list_objects(bucket, file_path)

    for ob in objects:
        return True
    return False


def upload(stream: bytes, file_path: str) -> bool:
    assert isinstance(stream, bytes)
    assert len(stream) > 0

    if exist(file_path):
        return False

    mime = get_file_mime(stream)

    client.put_object(
        bucket,
        file_path,
        BytesIO(stream),
        length=len(stream),
        content_type=mime
    )
    return True
