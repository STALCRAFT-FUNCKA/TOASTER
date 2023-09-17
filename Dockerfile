FROM python

LABEL author="Oidaho" email="oidahomain@gmail.com" version="2.1.2"

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]