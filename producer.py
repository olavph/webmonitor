from kafka import KafkaProducer

class Producer:
    def __init__(self, topic: str):
        self.topic = topic
        self.kafka_producer = KafkaProducer()

    def produce(self, event: str):
        self.kafka_producer.send(self.topic, event.encode())

    def flush(self):
        self.kafka_producer.flush()
