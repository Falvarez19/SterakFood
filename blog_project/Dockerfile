ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "jKqOj2R6SVH0kILwtTzpd3Bc2HRPwHo7dZJJT72bCNyJ0woiiv"

EXPOSE 8000

CMD ["gunicorn","--bind",":8000","--workers","2","blog_project.wsgi"]

RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput
