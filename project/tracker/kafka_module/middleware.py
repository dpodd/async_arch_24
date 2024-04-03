from threading import Thread


class StartKafkaConsumerMiddleware:
    consumer_thread_started = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not StartKafkaConsumerMiddleware.consumer_thread_started:
            StartKafkaConsumerMiddleware.consumer_thread_started = True

            thread = Thread(target=self.start_kafka_consumer)
            thread.daemon = True
            thread.start()

        response = self.get_response(request)
        return response

    def start_kafka_consumer(self):
        from .kafka_consumer import start_consumer
        start_consumer()
