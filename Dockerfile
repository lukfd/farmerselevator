FROM python:3.8-alpine

RUN apk add --no-cache musl-dev gcc libffi-dev g++

ENV FLASK_APP=farmerselevator

EXPOSE 8000

COPY . .

RUN pip install -r requirements.txt

CMD flask run --host=0.0.0.0 --port 8000
