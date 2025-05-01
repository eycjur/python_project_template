# Note: 可読性を重視した書き方をしているため、最適化はしていません
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# hadolint ignore=DL3008
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

WORKDIR /app

# ライブラリのインストール
# uv.lockが存在しないことを許容するため、./uv.lock*としている
COPY ./pyproject.toml ./uv.lock* /app/

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV PYTHONDONTWRITEBYTECODE=True
ENV PYTHONUNBUFFERED=True
ENV UV_LINK_MODE=copy

RUN uv sync --frozen --no-install-project

COPY ./app /app/app


# # CLI
# CMD ["python", "-m", "app.presentation.cli.app", "--help"]

# Dash
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${CONTAINER_PORT} --log-file - --access-logfile - --workers 1 --threads 4 --timeout 300 app.presentation.dash.index:server"]

# # FastAPI
# CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${CONTAINER_PORT} --log-file - --access-logfile - --workers 1 --threads 4 --timeout 300 -k uvicorn.workers.UvicornWorker app.presentation.fastapi.app:app"]

# # Flask
# CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${CONTAINER_PORT} --log-file - --access-logfile - --workers 1 --threads 4 --timeout 300 app.presentation.flask.app:app"]

# # Streamlit
# CMD ["sh", "-c", "python -m streamlit run app/presentation/streamlit/index.py --server.port ${CONTAINER_PORT}"]
