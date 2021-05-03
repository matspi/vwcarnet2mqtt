FROM python:3

RUN apt update && apt install -y git

ADD . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "main.py" ]