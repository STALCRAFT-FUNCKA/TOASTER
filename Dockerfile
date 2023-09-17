# python 3.10 base image
FROM python:3.10

# Information
LABEL author="Oidaho" email="oidahomain@gmail.com" version="2.1.2"

# env variables
ENV TOASTER_TOKER = $TOASTER_TOKER
ENV TOASTER_GROUPID = $TOASTER_GROUPID
ENV TOASTER_STUFFADMID = $TOASTER_STUFFADMID

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]