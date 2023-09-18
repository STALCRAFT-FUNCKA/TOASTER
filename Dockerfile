# python 3.10 base image
FROM python:3.10

# Information
LABEL author="Oidaho" email="oidahomain@gmail.com" version="2.1.2"

# env variables for usr_config
ARG TOKEN
ARG GROUPID
ARG STUFFADMID

ENV TOASTER_TOKEN = $TOKEN
ENV TOASTER_GROUPID = $GROUPID
ENV TOASTER_STUFFADMID = $STUFFADMID

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]