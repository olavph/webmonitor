from kafka import KafkaProducer

from webevent.webevent import WebEvent


class Producer:
    def __init__(self, topic: str):
        self.topic = topic
        self.kafka_producer = KafkaProducer()

    def send(self, event: WebEvent):
        self.kafka_producer.send(self.topic, event.encode())

    def flush(self):
        self.kafka_producer.flush()
