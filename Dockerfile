FROM python:3.10-slim-buster
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        curl \
        fonts-ipafont-gothic \
        gcc \
        git \
        locales \
        make \
        neovim \
        python3-dev \
        sudo \
        tzdata \
        vim \
        zsh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "ja_JP UTF-8" > /etc/locale.gen && \
    locale-gen ja_JP.UTF-8

ENV LANG=ja_JP.UTF-8
ENV LC_ALL=ja_JP.UTF-8
ENV TZ=Asia/Tokyo
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV PATH=/root/.local/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.create false

RUN mkdir /app
WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install

COPY ./src /app/src

EXPOSE ${APP_PORT}


# # CLI
# CMD python -m src.presentation.cli.app --help

# Dash
CMD	gunicorn \
        --bind "0.0.0.0:${APP_PORT}" \
        --log-file - \
        --access-logfile - \
        --workers 4 \
        --timeout 300 \
        src.presentation.dash.index:server

# # FastAPI
# CMD	gunicorn \
#         --bind "0.0.0.0:${APP_PORT}" \
#         --log-file - \
#         --access-logfile - \
#         --workers 4 \
#         --timeout 300 \
#         -k uvicorn.workers.UvicornWorker \
#         src.presentation.fastapi.app:app

# # Flask
# CMD	gunicorn \
#         --bind "0.0.0.0:${APP_PORT}" \
#         --log-file - \
#         --access-logfile - \
#         --workers 4 \
#         --timeout 300 \
#         src.presentation.flask.app:app

# # Streamlit
# CMD python -m streamlit run src/presentation/streamlit/home.py --server.port ${APP_PORT}
