
FROM python:3-alpine

WORKDIR /app

COPY python/requirements.txt ./
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev

COPY . ./

EXPOSE 8000

CMD [ "python", "api.py" ]
