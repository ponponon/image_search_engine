from core.redis.models import client
import settings


key = settings.REDIS_CONFIG.key


def add_clip_url(clip_url: str) -> bool:
    return client.cfAddNX(key, clip_url) == 1


def exist_clip_url(clip_url: str) -> bool:
    return client.cfExists(key, clip_url) == 1


def remove_clip_url(clip_url: str) -> None:
    client.cfDel(key, clip_url)


def create_filter():
    client.cfCreate(key, 1000000)
