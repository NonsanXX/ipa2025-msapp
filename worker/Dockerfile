FROM python

WORKDIR /home/worker

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer.py .
COPY worker.py .
COPY database.py .
COPY router_client.py .
COPY callback.py .

CMD ["python", "-u", "worker.py"]
