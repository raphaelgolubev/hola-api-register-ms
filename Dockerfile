# # Используем официальный образ Python
# FROM python:3.12.5-slim

# # Настраиваем Poetry
# ENV POETRY_VERSION=1.8.3
# ENV POETRY_HOME=/opt/poetry
# ENV POETRY_VENV=/opt/poetry-venv
# ENV POETRY_CACHE_DIR=/opt/.cache
# # Добавляем `poetry` в PATH
# ENV PATH="${PATH}:${POETRY_VENV}/bin"

# #Запрещает Python записывать файлы pyc на диск
# ENV PYTHONDONTWRITEBYTECODE 1
# #Запрещает Python буферизировать stdout и stderr
# ENV PYTHONUNBUFFERED 1
# # Устанавливаем временную зону контейнера
# ENV TZ=Europe/Moscow
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# # Устанавливаем рабочую директорию
# WORKDIR /app
# # Копируем файлы проекта, включая poetry.lock и pyproject.toml
# COPY . .


# # Устанавливаем зависимости
# # Установка setuptools избавляет от ошибки "No module named 'distutils'"
# RUN python3 -m venv $POETRY_VENV \
#     && $POETRY_VENV/bin/pip install --no-cache-dir -U pip setuptools \
#     && $POETRY_VENV/bin/pip install --no-cache-dir poetry==${POETRY_VERSION} \
#     && poetry config virtualenvs.create false \
#     && poetry install --no-dev --no-interaction --no-ansi

# # Указываем команду для запуска приложения
# CMD [ "poetry", "run", "python", "." ]


# ============================================= base
FROM python:3.12.5-slim AS base

# Запрещает Python записывать файлы pyc на диск
# Запрещает Python буферизировать stdout и stderr
# Устанавливаем временную зону контейнера
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Moscow

# Указываем рабочую директорию
WORKDIR /app

# ============================================= builder
FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_CACHE_DIR=/opt/.cache

# Копируем файлы poetry.lock и pyproject.toml для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Устанавливаем зависимости
RUN $POETRY_VENV/bin/poetry config virtualenvs.create false \
    && $POETRY_VENV/bin/poetry install --no-dev --no-interaction --no-ansi

# ============================================= final
FROM builder AS final

# Настраиваем временную зону контейнера
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# Прописываем путь до Poetry в PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"
# Копируем виртуальное окружение в контейнер
COPY --from=builder $POETRY_VENV $POETRY_VENV
# Копируем проект в контейнер
COPY . .

# Указываем команду для запуска приложения
CMD [ "poetry", "run", "python", "." ]
