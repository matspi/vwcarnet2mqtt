# VWCarNet2MQTT

## Information

Retrieve statistics about your car using 
the python package [volkswagncarnet](https://github.com/robinostlund/volkswagencarnet) and publish it over MQTT

I use it to feed my car's status into my home automation.

## Usage

Simply set three environment variables to the docker container and let it run:

    $ docker run -e VW_USERNAME=<email-address> -e VW_PASSWORD=<password> -e MQTT_HOST=<your.mqtt.broker> matthiasspiller/vwcarnet2mqtt

