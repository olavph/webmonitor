from kafka import KafkaConsumer

from webevent.webevent import WebEvent


class Consumer:
    """Consumer is an iterable to a stream of WebEvents

    It receives events from a Producer of the same topic.
    """

    def __init__(self, topic: str):
        """Initialize a KafkaConsumer

        Args:
            topic (str): Kafka topic
        """
        self.kafka_consumer = KafkaConsumer(topic)

    def __iter__(self):
        return self

    def __next__(self):
        return WebEvent.decode(next(self.kafka_consumer).value)
