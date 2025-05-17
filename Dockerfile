# Note: 可読性を重視した書き方をしているため、最適化はしていません
# 参考
# https://docs.astral.sh/uv/guides/integration/docker/#using-uv-in-docker
# https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.7.2 /uv /uvx /bin/

ENV DEBIAN_FRONTEND=noninteractive
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        fonts-ipafont-gothic \
        gcc \
        git \
        locales \
        make \
        neovim \
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

# システムのPythonを使用する
# cf. https://docs.astral.sh/uv/concepts/projects/config/#project-environment-path
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV UV_LINK_MODE=copy

WORKDIR /app

# 依存関係のインストール
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen  --no-install-project

# /app/app/...となるようにコピー
COPY ./app/ /app/app/

# # CLI
# CMD ["python", "-m", "app.presentation.cli.app", "--help"]

# Dash
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:${CONTAINER_PORT} --log-file - --access-logfile - --workers 1 --threads 4 --timeout 300 app.presentation.dash.index:server"]

# # FastAPI
# CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:${CONTAINER_PORT} --log-file - --access-logfile - --workers 1 --threads 4 --timeout 300 -k uvicorn.workers.UvicornWorker app.presentation.fastapi.app:app"]

# # Flask
# CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:${CONTAINER_PORT} --log-file - --access-logfile - --workers 1 --threads 4 --timeout 300 app.presentation.flask.app:app"]

# # Streamlit
# CMD ["/bin/bash", "-c", "python -m streamlit run app/presentation/streamlit/index.py --server.port ${CONTAINER_PORT}"]
