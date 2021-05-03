
import os
import asyncio
import pprint
import json
from aiohttp import ClientSession
from asyncio_mqtt import Client as MqttClient
import paho.mqtt.publish as publish
from vw_connection import Connection

VW_USERNAME = os.getenv("VW_USERNAME")
VW_PASSWORD = os.getenv("VW_PASSWORD")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
INTERVAL = int(os.getenv("INTERVAL", 300))


async def publish_vehicle(vehicle):
    uid = vehicle.unique_id
    topic = "vwcarnet/" + uid

    async with MqttClient(MQTT_HOST, MQTT_PORT) as mqtt:
        await mqtt.publish(topic, json.dumps(vehicle.attrs))


async def main():
    async with ClientSession(headers={'Connection': 'keep-alive'}) as session:
        connection = Connection(
            session, VW_USERNAME, VW_PASSWORD)
        if await connection.doLogin():
            while True:
                if await connection.update():
                    for vehicle in connection.vehicles:
                        a = vehicle.attrs
                        await publish_vehicle(vehicle)

                await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
