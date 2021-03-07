FROM python:3.9.2-slim-buster

RUN pip install -r requirements.txt
ADD . .
ENTRYPOINT [ "python", "main.py" ]