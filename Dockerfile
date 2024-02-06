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

EXPOSE ${APP_PORT}


# # CLI
# CMD python -m src.presentation.cli.app --help

# # Dash
# CMD python -m src.presentation.dash.index

# FastAPI
CMD	gunicorn \
        --bind "0.0.0.0:${APP_PORT}" \
        --log-file - \
        --access-logfile - \
        -k uvicorn.workers.UvicornWorker \
        src.presentation.fastapi.app:app

# # Flask
# CMD	gunicorn \
#         --bind "0.0.0.0:${APP_PORT}" \
#         --log-file - \
#         --access-logfile - \
#         src.presentation.flask.app:app

# # Streamlit
# CMD python -m streamlit run src/presentation/streamlit/home.py --server.port ${APP_PORT}
