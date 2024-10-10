FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV PORT=8000
ENV DEBUG=True

CMD ["gunicorn", "--worker-class", "eventlet", "--bind", "0.0.0.0:8000", "app:app"]