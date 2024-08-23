# Note: 可読性を重視した書き方をしているため、最適化はしていません
FROM python:3.12-slim-bookworm

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        curl \
        fonts-ipafont-gothic \
        gcc \
        g++ \
        git \
        locales \
        make \
        neovim \
        pandoc \
        python3-dev \
        sudo \
        tzdata \
        vim \
        zsh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 言語設定
RUN echo "ja_JP UTF-8" > /etc/locale.gen && \
    locale-gen ja_JP.UTF-8
ENV LANG=ja_JP.UTF-8
ENV LC_ALL=ja_JP.UTF-8
ENV TZ=Asia/Tokyo

# poetryのインストール
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV PATH=/root/.local/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.create false

WORKDIR /app

# ライブラリのインストール
# poetry.lockが存在しないことを許容するため、./poetry.lock*としている
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-interaction --no-ansi

COPY ./src /app/src


# # CLI
# CMD ["python", "-m", "src.presentation.cli.app", "--help"]

# Dash
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${CONTAINER_PORT} --log-file - --access-logfile - --workers 1 --threads 4 --timeout 300 src.presentation.dash.index:server"]

# # FastAPI
# CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${CONTAINER_PORT} --log-file - --access-logfile - --workers 1 --threads 4 --timeout 300 -k uvicorn.workers.UvicornWorker src.presentation.fastapi.app:app"]

# # Flask
# CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${CONTAINER_PORT} --log-file - --access-logfile - --workers 1 --threads 4 --timeout 300 src.presentation.flask.app:app"]

# # Streamlit
# CMD ["sh", "-c", "python -m streamlit run src/presentation/streamlit/home.py --server.port ${CONTAINER_PORT}"]
