FROM python:3.9-slim
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y libpq-dev gcc
WORKDIR /app
COPY requirements.txt ./
RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]