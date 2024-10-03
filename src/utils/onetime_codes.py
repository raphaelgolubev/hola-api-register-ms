from redis.asyncio import Redis

from src.config import settings


class OneTimeCodeService:
    def __init__(self):
        self.client = Redis()