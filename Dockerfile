FROM python:3.8.13-buster

ENV APP_PATH=/code

RUN pip install poetry && \
    poetry config virtualenvs.create false

WORKDIR $APP_PATH

# poetry
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install

COPY ./local-redash ./local-redash
