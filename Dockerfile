# ベースイメージ
FROM python:3.10-slim-buster
WORKDIR /app

RUN apt update && apt install -y git vim zsh neovim sudo
RUN python -m pip install -U pip poetry
COPY pyproject.toml poetry.lock ./
RUN python -m poetry install --no-interaction

ARG ROOT_PASSWORD=pass
RUN echo "root:${ROOT_PASSWORD}" | chpasswd

ARG DOCKER_UID=1000
ARG DOCKER_USER=docker_user
ARG DOCKER_PASSWORD=pass
RUN useradd -m --uid ${DOCKER_UID} --groups sudo ${DOCKER_USER} \
    && echo "${DOCKER_USER}:${DOCKER_PASSWORD}" | chpasswd

USER ${DOCKER_USER}
