FROM python:3.11-slim

RUN pip install --upgrade pip --no-cache-dir

WORKDIR /app

RUN pip install gunicorn==20.1.0
RUN apt-get update && apt-get install -y locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

COPY requirements.txt ./

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "music_shop.wsgi", "--bind", "0.0.0.0:10000"]