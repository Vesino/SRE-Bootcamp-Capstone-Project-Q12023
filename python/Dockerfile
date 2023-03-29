
FROM python:3-alpine

WORKDIR /app

COPY python/requirements.txt ./
RUN apk add --no-cache python3-dev libffi-dev libev-dev gcc musl-dev make && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn gevent && \
    pip install --no-cache-dir -r requirements.txt


COPY . ./

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "api:create_app()"]
