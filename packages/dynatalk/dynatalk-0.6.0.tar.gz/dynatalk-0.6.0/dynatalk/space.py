import json
import os
import traceback

import paho.mqtt.client as mqtt


class MQTTSpace:
    """
    I am responsible for sending and receiving messages and understand the details of the message transmission (MQTT), but I do not understand the content of the message. Whenever I receive a message, I will forward it to the supervisor
    """

    def __init__(self, supervisor) -> None:
        self.supervisor = supervisor

        # env
        host = os.environ.get("MQTT_HOST", "127.0.0.1")
        port = int(os.environ.get("MQTT_PORT", 1883))
        username = os.environ.get("MQTT_USERNAME", "guest")
        password = os.environ.get("MQTT_PASSWORD", "test")

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.onConnect
        self.mqtt_client.on_message = self.onMessage
        self.mqtt_client.username_pw_set(username, password)
        self.mqtt_client.connect(host, port, 60)
        self.mqtt_client.loop_start()  # non-blocking

    # The callback for when the client receives a CONNACK response from the server.
    def onConnect(self, client, userdata, flags, rc):
        # print("Connected with result code " + str(rc))
        if rc == 0:
            print("Connected to MQTT broker successfully")
        else:
            print(f"Connection to MQTT broker failed with error code {rc}")
        self.mqtt_client.subscribe("+", qos=1)

    def onMessage(self, client, userdata, msg) -> None:
        # Avoid MQTT threads being broken
        try:
            self.supervisor.onMessage(msg.topic, msg.payload)
        except Exception as e:
            print(traceback.format_exc())

    def publish(self, topic, payload) -> None:
        # publish(topic, payload=None, qos=0, retain=False)
        self.mqtt_client.publish(topic, payload, qos=1)
