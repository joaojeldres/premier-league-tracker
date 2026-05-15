FROM python:3.9-slim

WORKDIR /app

COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt

ENV PIP_PROGRESS_BAR=off

RUN python -m pip install --upgrade pip --no-cache-dir --progress-bar off
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

CMD ["python", "app.py"]
