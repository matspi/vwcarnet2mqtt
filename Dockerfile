FROM python:3.9.2-slim-buster

ADD . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "main.py" ]