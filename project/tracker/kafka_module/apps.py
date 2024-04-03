from django.apps import AppConfig

from .kafka_consumer import run_consumer_as_thread


class KafkaConfig(AppConfig):
    name = 'kafka_module'

    # def ready(self):
    #     run_consumer_as_thread()
