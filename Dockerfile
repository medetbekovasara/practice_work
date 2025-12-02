FROM python:3.9-alpine3.16

# ВАЖНО: полный набор зависимостей для psycopg2 и celery
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    postgresql-dev \
    postgresql-client \
    libffi-dev \
    openssl-dev \
    linux-headers \
    cargo \
    build-base

# Указываем рабочую директорию
WORKDIR /service

# Copy requirements
COPY requirements.txt /temp/requirements.txt

# Установка Python зависимостей
RUN pip install --upgrade pip && pip install --no-cache-dir -r /temp/requirements.txt

# Copy Django project
COPY service /service

# Создать пользователя
RUN adduser -D service-user
USER service-user

EXPOSE 8000
