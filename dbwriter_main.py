#!/bin/env python3

import signal
import sys

from dbwriter import DBWriter
from webevent import WebEvent

TOPIC_NAME = "web_monitor"
DB_NAME = "mydb"
TABLE_NAME = "web_events"
CREATE_TABLE_QUERY = f"CREATE TABLE {TABLE_NAME} (id serial PRIMARY KEY, url varchar, status_code integer, response_time real, match_found bool, match varchar)"
INSERT_QUERY = f"INSERT INTO {TABLE_NAME} (url, status_code, response_time, match_found, match) VALUES (%s, %s, %s, %s, %s)"
DECODE_FUNCTION = WebEvent.decode


def signal_handler(sig, frame):
    print("Stopping DBWriter")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    writer = DBWriter(TOPIC_NAME, DB_NAME, CREATE_TABLE_QUERY, INSERT_QUERY, DECODE_FUNCTION)
    writer.run()


if __name__ == "__main__":
    main()
