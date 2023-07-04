from redisbloom.client import Client
import settings

client = Client(
    host=settings.REDIS_CONFIG.host,
    port=settings.REDIS_CONFIG.port,
    db=settings.REDIS_CONFIG.db
)
