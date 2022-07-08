FROM python:3.9.13-slim

WORKDIR /usr/src/app

ENV PYTHONPATH ./app/:$PYTHONPATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
   && apt-get install -y python3-dev gcc musl-dev libffi-dev netcat

RUN pip install --upgrade pip
COPY ./requirements ./requirements
RUN pip install -r requirements/local.txt

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
