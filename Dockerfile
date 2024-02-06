FROM python:3.10-slim-buster
RUN apt-get update && \
    apt-get install --no-install-recommends -y curl gcc python3-dev git make vim zsh neovim sudo

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH
RUN poetry config virtualenvs.create false

RUN mkdir /app
WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
RUN poetry install

COPY ./src /app/src

EXPOSE ${PORT}

CMD	gunicorn \
        --bind "0.0.0.0:${PORT}" \
        --log-file - \
        --access-logfile - \
        -k uvicorn.workers.UvicornWorker \
        --timeout 180 \
        src.app:app
