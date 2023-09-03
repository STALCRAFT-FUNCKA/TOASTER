FROM python

WORKDIR /root/TOASTER

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "main.py"]