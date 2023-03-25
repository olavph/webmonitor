from kafka import KafkaConsumer

from webevent.webevent import WebEvent


class Consumer:
    def __init__(self, topic: str):
        self.kafka_consumer = KafkaConsumer(topic)

    def __iter__(self):
        return self

    def __next__(self):
        return WebEvent.decode(next(self.kafka_consumer).value)
