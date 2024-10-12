FROM python:3.12

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install git iproute2 procps lsb-release

COPY ../.  /workspace

# Install poetry and python dependencies
ENV POETRY_VERSION=1.8.0
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false \
    && cd /workspace/backend && poetry install

# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=
