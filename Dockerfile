FROM python:3.9-slim AS install-deps

WORKDIR /app

COPY ./scripts .

CMD ./scripts/run.sh
EXPOSE 5000

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt


FROM install-deps as copy-files

COPY . .
