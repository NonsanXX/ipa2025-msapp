FROM python

WORKDIR /home/scheduler

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY database.py .
COPY producer.py .
COPY scheduler.py .


CMD ["python", "-u", "scheduler.py"]
