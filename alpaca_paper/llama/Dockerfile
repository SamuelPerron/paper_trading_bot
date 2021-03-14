FROM python:3.7

WORKDIR /api

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get install gcc

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
COPY . .
CMD ["flask", "run"]
