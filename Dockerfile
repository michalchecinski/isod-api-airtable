FROM python:3.6.8

ENV TZ=Europe/Warsaw

ARG airtable_key
ENV AIRTABLE_API_KEY=$airtable_key

ARG isod_key
ENV ISOD_API_KEY=$isod_key

RUN apt-get update \
    && apt-get install -y cron \
    && apt-get autoremove -y

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

COPY ./cronpy /etc/cron.d/cronpy
CMD ["cron", "-f"]