FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY ./src /app/src

EXPOSE 8000

CMD [ "uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
