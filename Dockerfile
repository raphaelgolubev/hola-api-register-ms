# Используем официальный образ Python
FROM python:3.12.5-slim

# Настраиваем Poetry
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
# Добавляем `poetry` в PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

#Запрещает Python записывать файлы pyc на диск
ENV PYTHONDONTWRITEBYTECODE 1
#Запрещает Python буферизировать stdout и stderr
ENV PYTHONUNBUFFERED 1
# Устанавливаем временную зону контейнера
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# Устанавливаем рабочую директорию
WORKDIR /app
# Копируем файлы проекта, включая poetry.lock и pyproject.toml
COPY . .


# Устанавливаем зависимости
# Установка setuptools избавляет от ошибки "No module named 'distutils'"
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install --no-cache-dir -U pip setuptools \
    && $POETRY_VENV/bin/pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Указываем команду для запуска приложения
CMD [ "poetry", "run", "python", "." ]
