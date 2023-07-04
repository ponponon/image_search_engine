import hashlib
from pathlib import Path


def get_file_md5(video_filepath: Path) -> str:
    """ 返回一个长度为 32 的字符串 """
    md5_encoder = hashlib.md5()
    with open(video_filepath, 'rb') as f:
        md5_encoder.update(f.read())
        return md5_encoder.hexdigest()


def get_string_md5(text: str) -> str:
    md5_encoder = hashlib.md5()
    md5_encoder.update(text.encode('utf-8'))
    return md5_encoder.hexdigest()


def get_stream_md5(stream: bytes) -> str:
    md5_encoder = hashlib.md5()
    md5_encoder.update(stream)
    return md5_encoder.hexdigest()
