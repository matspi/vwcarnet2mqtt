FROM python:3.9.2-slim-buster

RUN pip install volkswagencarnet asyncio-mqtt
ADD . .
ENTRYPOINT [ "python", "main.py" ]