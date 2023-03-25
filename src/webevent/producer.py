from kafka import KafkaProducer

from webevent.webevent import WebEvent


class Producer:
    """Producer sends WebEvents to Consumers of the same topic
    """

    def __init__(self, topic: str):
        """Initialize a KafkaProducer

        Args:
            topic (str): Kafka topic
        """
        self.topic = topic
        self.kafka_producer = KafkaProducer()

    def send(self, event: WebEvent):
        """Queue event to be sent to Consumers

        Args:
            event (WebEvent): generated event
        """
        self.kafka_producer.send(self.topic, event.encode())

    def flush(self):
        """Send all queued events to Consumers
        """
        self.kafka_producer.flush()
