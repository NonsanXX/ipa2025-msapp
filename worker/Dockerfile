FROM python

WORKDIR /home/worker

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker.py .
COPY database.py .
COPY get_interfaces.py .

CMD ["python", "-u", "worker.py"]
