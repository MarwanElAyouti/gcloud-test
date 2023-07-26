FROM python:3.10-slim-buster
WORKDIR /code/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc 
RUN pip install poetry==1.5.0

COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./ /code

# Copying start commands
COPY ./start-webserver.sh /start-webserver.sh

# Allowing to run bash scripts
RUN chmod 777 /start-webserver.sh

CMD /start-webserver.sh
