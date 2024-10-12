FROM python:3.12

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install git iproute2 procps lsb-release

WORKDIR /app/
COPY ../.  /app

# Install poetry and python dependencies
ENV POETRY_VERSION=1.8.0
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false \
    && cd /app && poetry install

# Clean up
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
