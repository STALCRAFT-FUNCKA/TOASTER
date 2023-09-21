# python 3.10 base image
FROM python:3.10

# Information
LABEL author="Oidaho" email="oidahomain@gmail.com"

WORKDIR /toaster

ARG TOKEN
ARG ID
ARG ADM

ENV TOASTER_TOKEN $TOKEN
ENV TOASTER_GROUPID $ID
ENV TOASTER_STAFFADMID $ADM

ARG HOST
ARG PORT
ARG USER
ARG PASSWORD

ENV SQL_HOST $HOST
ENV SQL_PORT $PORT
ENV SQL_USER $USER
ENV SQL_PASSWORD $PASSWORD

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "main.py"]