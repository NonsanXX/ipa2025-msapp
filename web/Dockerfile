FROM python

WORKDIR /home/myapp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./static ./static
COPY ./templates ./templates
COPY app.py .

EXPOSE 8080

CMD ["python", "-u", "app.py"]
