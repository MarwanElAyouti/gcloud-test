FROM python:3.10-slim-buster as base

WORKDIR /code/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc 
RUN pip install poetry==1.1.11

COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./ /code


# Dev target for CI/CD validate
FROM base as dev
RUN apt-get install -y make
