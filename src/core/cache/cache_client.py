import json
import logging
from typing import Any

import redis.asyncio as redis

from src.core.config import settings

logger = logging.getLogger(__name__)


class CacheClient:
    _instance = None
    redis_client: redis.Redis | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def start(self):
        """앱 시작 시 Redis 연결"""
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
            # 연결 테스트
            await self.redis_client.ping()
            logger.info("Redis Cache connected.")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")

    async def stop(self):
        """앱 종료 시 연결 해제"""
        if self.redis_client:
            await self.redis_client.aclose()
            logger.info("Redis Cache disconnected.")

    async def get(self, key: str) -> Any:
        """캐시 조회 (JSON 파싱 포함)"""
        if not self.redis_client:
            return None
        try:
            val = await self.redis_client.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.error(f"Cache GET error key={key}: {e}")
        return None

    async def set(self, key: str, value: Any, ttl: int = 300):
        """캐시 저장 (JSON 직렬화 포함, 기본 5분 유지)"""
        if not self.redis_client:
            return
        try:
            json_val = json.dumps(value, default=str)  # datetime 등 처리를 위해 default=str
            await self.redis_client.setex(key, ttl, json_val)
        except Exception as e:
            logger.error(f"Cache SET error key={key}: {e}")

    async def delete_pattern(self, pattern: str):
        """패턴에 맞는 키 삭제 (Invalidation 용)"""
        if not self.redis_client:
            return
        try:
            # SCAN을 사용하여 블로킹 없이 키 검색
            keys = []
            async for key in self.redis_client.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                await self.redis_client.delete(*keys)
                logger.info(f"Invalidated cache keys pattern: {pattern}")
        except Exception as e:
            logger.error(f"Cache invalidation error pattern={pattern}: {e}")
