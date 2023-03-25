# ベースイメージ
FROM --platform=linux/amd64 python:3.10

RUN apt-get update && \
    apt-get install -y gcc git make vim zsh neovim sudo

## for development
COPY requirements.txt /tmp/requirements.txt
RUN pip install -U pip && \
    pip install -r /tmp/requirements.txt
# RUN python -m pip install -U pip poetry
# COPY pyproject.toml poetry.lock ./
# RUN python -m poetry install --no-interaction

ADD https://api.github.com/repos/eycjur/dotfiles/git/refs/heads/main version.json
RUN git clone https://github.com/eycjur/dotfiles.git ~/dotfiles
RUN ~/dotfiles/install.sh

# CMD ["/bin/zsh"]


## for web app
WORKDIR /app
COPY ./app .
COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

CMD exec gunicorn \
    --bind :$PORT \
    --workers 1 \
    --threads 8 \
    --timeout 0 \
    --reload \
    -k uvicorn.workers.UvicornWorker \
    app:app
