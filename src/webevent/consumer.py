import time

import kafka

from webevent.webevent import WebEvent


class Consumer:
    """Consumer is an iterable to a stream of WebEvents

    It receives events from a Producer of the same topic.
    """

    def __init__(self, topic: str, host: str, port: int, **kwargs):
        """Initialize a KafkaConsumer, waiting for the broker to be available

        For keyword args, see https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html

        Args:
            topic (str): Kafka topic
            host (str): Kafka broker host name
            port (str): Kafka broker port number
        """
        self.kafka_consumer = None
        while self.kafka_consumer is None:
            try:
                self.kafka_consumer = kafka.KafkaConsumer(topic, bootstrap_servers=f"{host}:{port}", **kwargs)
            except kafka.errors.NoBrokersAvailable:
                print("No brokers available, retrying")
                time.sleep(1)

    def __iter__(self):
        return self

    def __next__(self):
        return WebEvent.decode(next(self.kafka_consumer).value)
