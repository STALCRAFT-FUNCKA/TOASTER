# python 3.10 base image
FROM python:3.10

# Information
LABEL author="Oidaho" email="oidahomain@gmail.com" version="2.1.2"

WORKDIR /app

ARG TOKEN
ARG ID
ARG ADM

ENV TOASTER_TOKEN = $TOKEN
ENV TOASTER_GROUPID = $ID
ENV TOASTER_STUFFADMID = $ADM

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]