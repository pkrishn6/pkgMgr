FROM python:3.6-slim

ARG REQUIREMENTS=requirements.txt
ARG PROJECT_PATH="/opt/server"

RUN apt-get update && \
    apt-get install -y \
        procps \
        curl && \
    apt-get clean

# Install project dependencies
COPY requirements* /
RUN pip install --no-cache-dir -r ${REQUIREMENTS}

COPY server/ $PROJECT_PATH

ENV DEFAULT_LOG_FORMAT="[%(asctime)s:%(process)d %(thread)d %(module)s#L%(lineno)d:%(levelname)s]: %(message)s"
ENV DEFAULT_LOG_LEVEL="INFO"
ENV DJANGO_ENV="dev"
ENV DJANGO_PROJECT_PATH="$PROJECT_PATH"
WORKDIR $PROJECT_PATH
