
FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
RUN apk add --no-cache python3-dev libffi-dev libev-dev gcc musl-dev make && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn gevent && \
    pip install --no-cache-dir -r requirements.txt


COPY . ./

EXPOSE 8000

CMD [ "gunicorn", "app:app" ]
