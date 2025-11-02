FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r Lab4DB/requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENV PYTHONPATH="/app/Lab4DB:${PYTHONPATH}"
CMD ["flask", "run"]
