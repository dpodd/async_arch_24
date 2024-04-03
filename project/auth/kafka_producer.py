import enum
from enum import auto
import json

from django.conf import settings
from kafka import KafkaProducer


class _Enam(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


class EventType(_Enam):
    USER_CREATED = auto()
    USER_UPDATED = auto()
    USER_DELETED = auto()

    # business events
    USER_ROLE_CHANGED = auto()


# producer = KafkaProducer(
#     bootstrap_servers=[settings.KAFKA_BROKER],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

import time


def create_kafka_producer(retries=5, wait=3):
    """Attempt to create a KafkaProducer with retries."""
    for _ in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=[settings.KAFKA_BROKER],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            return producer
        except Exception as e:
            print(f"Failed to connect to Kafka: {e}, retrying in {wait} seconds...")
            time.sleep(wait)
    raise Exception("Failed to create KafkaProducer after retries")


# Attempt to create a Kafka producer with retry logic
producer = create_kafka_producer()


class KafkaProducerService:
    @staticmethod
    def send_event(topic, event):
        producer.send(topic, event)
        producer.flush()
