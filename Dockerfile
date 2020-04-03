FROM python:latest

RUN apt-get update && apt-get install -y python-dev libmariadb-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./ .

CMD /usr/local/bin/python main.py
