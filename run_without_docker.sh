#!/bin/env bash
set -e

export KAFKA_HOST=kafka
export KAFKA_PORT=9092
# export KAFKA_SECURITY_PROTOCOL=
# export KAFKA_SSL_CAFILE=
# export KAFKA_SSL_CERTFILE=
# export KAFKA_SSL_KEYFILE=
export DB_NAME=postgres
export DB_HOST=postgres
export DB_PORT=5432
export DB_USER=postgres
# export DB_PASSWORD=
export DB_SSLMODE=disable

# Based on https://stackoverflow.com/a/2173421
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

./src/start_webmonitor.py &
./src/start_dbwriter.py
