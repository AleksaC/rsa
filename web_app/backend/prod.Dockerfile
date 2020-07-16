FROM python:3.8-alpine as base

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    git

RUN adduser -D -u 1000 appuser

WORKDIR /home/appuser/app

USER appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV PATH="/home/appuser/.local/bin:$PATH"

CMD gunicorn \
    --workers=$((2 * $(getconf _NPROCESSORS_ONLN) + 1)) \
    --bind 0.0.0.0:5000 \
    app:app
