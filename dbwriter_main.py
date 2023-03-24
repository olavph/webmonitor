#!/bin/env python3

import signal
import sys

from dbwriter import DBWriter

TOPIC_NAME = "web_monitor"
DB_NAME = "mydb"
CREATE_TABLE_QUERY = "CREATE TABLE test (id serial PRIMARY KEY, url varchar, status_code integer, response_time real, match_found bool, match varchar)"
INSERT_QUERY = "INSERT INTO test (url, status_code, response_time, match_found, match) VALUES (%s, %s, %s, %s, %s)"


def signal_handler(sig, frame):
    print("Stopping DBWriter")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    writer = DBWriter(TOPIC_NAME, DB_NAME, CREATE_TABLE_QUERY, INSERT_QUERY)
    writer.run()


if __name__ == "__main__":
    main()
