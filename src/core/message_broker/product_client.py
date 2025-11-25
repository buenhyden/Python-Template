import json
import logging

from aiokafka import AIOKafkaProducer

from src.core.config import settings

logger = logging.getLogger(__name__)


class KafkaProducerClient:
    _instance = None
    producer: AIOKafkaProducer | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def start(self):
        """앱 시작 시 프로듀서 초기화"""
        try:
            # [변경] settings.KAFKA_BROKERS 리스트를 직접 전달
            self.producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKERS)
            await self.producer.start()
            logger.info(f"Kafka Producer started. Brokers: {settings.KAFKA_BROKERS}")
        except Exception as e:
            logger.error(f"Failed to start Kafka Producer: {e}")

    async def stop(self):
        """앱 종료 시 연결 해제"""
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka Producer stopped.")

    async def send_message(self, topic: str, message: dict):
        """메시지 전송"""
        if not self.producer:
            logger.warning("Kafka Producer is not initialized.")
            return

        try:
            # JSON 직렬화 및 UTF-8 인코딩
            value_json = json.dumps(message).encode("utf-8")
            await self.producer.send_and_wait(topic, value_json)
            logger.info(f"Sent message to topic {topic}: {message}")
        except Exception as e:
            logger.error(f"Failed to send message to Kafka: {e}")
            raise e
