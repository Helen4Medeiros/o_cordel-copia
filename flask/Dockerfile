## BASE IMAGE ##
FROM python:3.13.14-slim-bookworm AS base

WORKDIR /usr/src/cordel/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip

# demais dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# arquivos da aplicação
COPY config.py .
COPY app/ ./app
COPY run.py .

## DEV IMAGE ##
FROM base AS dev

# depurador Python
RUN pip install --no-cache-dir debugpy

CMD ["/bin/bash", "-c", "python3 -m debugpy --listen 0.0.0.0:5678 -m flask run --host=0.0.0.0 --port 5000 --debug"]

## PRODUCTION IMAGE ##
FROM base AS prod

RUN pip install --no-cache-dir gunicorn==22.0.0

# Criando usuário para que o contêiner não execute como root
RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --uid 1001 --system --group app
RUN chown -R app:app .
USER app