FROM python:3.6.8-slim

ENV TZ=Europe/Warsaw

RUN apt-get update \
    && apt-get install -y cron \
    && apt-get autoremove -y

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

COPY ./cronpy /etc/cron.d/cronpy
RUN crontab /etc/cron.d/cronpy

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cronpy

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
