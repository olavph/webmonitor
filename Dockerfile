# Based on https://aka.ms/vscode-docker-python
FROM fedora:37

RUN dnf -y update && dnf -y install python python3-pip && dnf clean all

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["./src/start_webmonitor.py"]
