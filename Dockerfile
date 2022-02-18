# ベースイメージ
FROM python:3.10-slim-buster
WORKDIR /app

RUN apt-get update && apt-get install -y git vim zsh neovim sudo
RUN python -m pip install -U pip poetry
COPY pyproject.toml poetry.lock ./
RUN python -m poetry install --no-interaction

ARG DOCKER_UID=1000
ARG DOCKER_USER=user
ARG DOCKER_PASSWORD=pass
RUN useradd -m --uid ${DOCKER_UID} --groups sudo ${DOCKER_USER} \
    && echo "${DOCKER_USER}:${DOCKER_PASSWORD}" | chpasswd

USER ${DOCKER_USER}

RUN git clone https://github.com/eycjur/dotfiles.git ~/dotfiles
ENV SHELL /usr/bin/zsh
RUN ~/dotfiles/install.sh

CMD ["/bin/zsh"]
