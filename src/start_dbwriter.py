#!/bin/env python3
"""Start a DBWriter that receives events from a Kafka topic and writes
them to a PostgresSQL, until SIGINT is received.
"""

import os
import signal
import sys

from webevent.consumer import Consumer
from webevent.dbwriter import DBWriter
from webevent.webevent import WebEvent

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT = os.getenv("KAFKA_PORT", 9092)
TOPIC_NAME = "webmonitor"
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_USER = "postgres"
DB_NAME = "webmonitor"
TABLE_NAME = "web_events"


def signal_handler(sig, frame):
    print("Stopping DBWriter")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Starting DBWriter")
    consumer = Consumer(KAFKA_HOST, KAFKA_PORT, TOPIC_NAME)
    writer = DBWriter(consumer, DB_HOST, DB_PORT, DB_USER, DB_NAME, TABLE_NAME, WebEvent)
    writer.run()


if __name__ == "__main__":
    main()
