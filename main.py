
import os
import asyncio
import pprint
import json
from aiohttp import ClientSession
from asyncio_mqtt import Client as MqttClient
import paho.mqtt.publish as publish
from vw_connection import Connection
import datetime
import pandas as pd

VW_USERNAME = os.getenv("VW_USERNAME")
VW_PASSWORD = os.getenv("VW_PASSWORD")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
INTERVAL = int(os.getenv("INTERVAL", 300))


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)


async def publish_vehicle(vehicle):
    uid = vehicle.unique_id
    base_topic = "vwcarnet/" + uid

    data = vehicle.attrs
    data = pd.json_normalize(data, sep='/').to_dict(orient='records')[0]

    async with MqttClient(MQTT_HOST, MQTT_PORT) as mqtt:
        for key in data:
            await mqtt.publish(base_topic + "/" + key, json.dumps(data[key], cls=DateTimeEncoder))


async def main():
    async with ClientSession(headers={'Connection': 'keep-alive'}) as session:
        connection = Connection(
            session, VW_USERNAME, VW_PASSWORD)
        if await connection.doLogin():
            while True:
                if await connection.update():
                    for vehicle in connection.vehicles:
                        await publish_vehicle(vehicle)

                await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# %%
