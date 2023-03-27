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


TOPIC_NAME = "webmonitor"
KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT = os.getenv("KAFKA_PORT", 9092)
KAFKA_SECURITY_PROTOCOL=os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
KAFKA_SSL_CAFILE=os.getenv("KAFKA_SSL_CAFILE", None)
KAFKA_SSL_CERTFILE=os.getenv("KAFKA_SSL_CERTFILE", None)
KAFKA_SSL_KEYFILE=os.getenv("KAFKA_SSL_KEYFILE", None)
TABLE_NAME = "web_events"
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", None)
DB_SSLMODE = os.getenv("DB_SSLMODE", None)


def signal_handler(sig, frame):
    print("Stopping DBWriter")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Starting DBWriter")
    consumer = Consumer(TOPIC_NAME, KAFKA_HOST, KAFKA_PORT,
                        security_protocol=KAFKA_SECURITY_PROTOCOL,
                        ssl_cafile=KAFKA_SSL_CAFILE,
                        ssl_certfile=KAFKA_SSL_CERTFILE,
                        ssl_keyfile=KAFKA_SSL_KEYFILE,
    )
    writer = DBWriter(consumer, TABLE_NAME, WebEvent,
                      DB_NAME, DB_HOST, DB_PORT, DB_USER,
                      password=DB_PASSWORD, sslmode=DB_SSLMODE)
    writer.run()


if __name__ == "__main__":
    main()
