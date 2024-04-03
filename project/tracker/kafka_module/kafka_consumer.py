from kafka import KafkaConsumer
import json
import threading

from kafka import KafkaConsumer
import logging
import json

import enum
from enum import auto
import json

from django.conf import settings

from . import events_processing

logger = logging.getLogger(__name__)


class _Enam(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


class EventType(_Enam):
    USER_CREATED = auto()
    USER_UPDATED = auto()
    USER_DELETED = auto()

    # business events
    USER_ROLE_CHANGED = auto()


def process_message(message):
    data = message.value
    event_type = data.get("type")
    user_data = data

    if event_type == EventType.USER_UPDATED.value:
        logger.info(f"Updating user {user_data['public_id']}'s role to {user_data['role']}")
        events_processing.process_user_updated_event(user_data=user_data)

    elif event_type == EventType.USER_DELETED.value:
        logger.info(f"Deleting user {user_data['public_id']}")
        events_processing.process_user_deleted_event(user_data=user_data)


def start_consumer():
    logger.info("Starting consumer...")

    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=[settings.KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        # group_id='tracker-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        process_message(message)
