import time

import kafka

from webevent.webevent import WebEvent


class Producer:
    """Producer sends WebEvents to Consumers of the same topic
    """

    def __init__(self, topic: str, host: str, port: int, **kwargs):
        """Initialize a KafkaProducer, waiting for the broker to be available

        For keyword args, see https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html

        Args:
            host (str): Kafka broker host name
            port (str): Kafka broker port number
            topic (str): Kafka topic
        """
        self.topic = topic

        self.kafka_producer = None
        while self.kafka_producer is None:
            try:
                self.kafka_producer = kafka.KafkaProducer(bootstrap_servers=f"{host}:{port}", **kwargs)
            except kafka.errors.NoBrokersAvailable:
                print("No brokers available, retrying")
                time.sleep(1)

    def send(self, event: WebEvent):
        """Send event to Consumers

        Args:
            event (WebEvent): generated event
        """
        self.kafka_producer.send(self.topic, event.encode())
