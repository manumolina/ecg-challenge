FROM python:3.10-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
    pip install pipenv

COPY /pyproject.toml .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]