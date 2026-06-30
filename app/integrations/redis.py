from redis import ConnectionPool, Redis

from app import settings

redis_pool = ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=0,
    protocol=2,
    socket_timeout=10,
    socket_connect_timeout=10,
    socket_keepalive=False,
    health_check_interval=0,
    max_connections=5,
)

redis_client = Redis(connection_pool=redis_pool, decode_responses=True)


class RedisService:
    """
    Redis service for dependency injection.
    """

    def __init__(self):
        self.client = redis_client

    def set_value(self, key: str, value: str, expire: int = None) -> None:
        self.client.set(name=key, value=value, ex=expire)

    def get_value(self, key: str) -> str:
        value = self.client.get(name=key)
        return value if value else None

    def delete_value(self, key: str) -> None:
        self.client.delete(key)
