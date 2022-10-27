# ベースイメージ
FROM python:3.10

RUN apt update && apt install -y gcc git make vim zsh neovim sudo

COPY requirements.txt /tmp/requirements.txt
RUN pip install -U pip && \
    pip install -r /tmp/requirements.txt
# RUN python -m pip install -U pip poetry
# COPY pyproject.toml poetry.lock ./
# RUN python -m poetry install --no-interaction

ADD https://api.github.com/repos/eycjur/dotfiles/git/refs/heads/main version.json
RUN git clone https://github.com/eycjur/dotfiles.git ~/dotfiles
RUN ~/dotfiles/install.sh

CMD ["/bin/zsh"]
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --reload app.app:app
# CMD ["uvicorn", "app.app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
