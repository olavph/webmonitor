# WebMonitor

This project, when run, monitors a set of website URLs, pushing their metrics to a Kafka topic.

The topic is also observed and written to a PostgresSQL database.

# Build

A single container needs to be built, the others will be pulled with the compose setup. If you don't have docker, refer to [installing docker](#installing-docker).

```bash
sudo docker build . --tag webmonitor
```

# Run

To run everything locally, including Kafka and PostgreSQL, execute:

```bash
sudo docker compose -f docker-compose-local.yml up -d
```

To run only the WebMonitor, substitute the host and port variables in `docker-compose.yml` and execute:

```bash
sudo docker compose -f docker-compose.yml up -d
```

# Run tests

```bash
cd src
python -m unittest test/test_*
```

# Installing docker

For more details, see https://docs.docker.com/engine/install/

```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager \
    --add-repo \
    https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# If prompted to accept the GPG key, verify that the fingerprint matches 060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35, and if so, accept it.
sudo systemctl start docker
```
