FROM python:3.12-slim

WORKDIR /app

COPY load_test.py .

RUN pip install requests

CMD ["python", "load_test.py"]
